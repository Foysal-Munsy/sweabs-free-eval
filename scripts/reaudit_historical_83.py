#!/usr/bin/env python3
"""Re-audit 83 original SWE-ABS augmented-test records from raw archived GitHub artifacts.

Produces an evidence CSV, append-only correction table and versioned 198-row CSV.
Does not overwrite the archived baseline or rerun tests.
"""
import argparse, csv, json, zipfile, pathlib, re, hashlib, collections
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--evidence-dir', type=pathlib.Path, required=True, help='directory holding sweabs-result-SAMPLE-OFFSET.zip files')
parser.add_argument('--checkpoint', type=pathlib.Path, default=pathlib.Path('results/2026-11-12/sweabs_samples1_2_first83_cumulative.csv'))
parser.add_argument('--baseline', type=pathlib.Path, default=pathlib.Path('results/2026-11-12/sweabs_full_198_cumulative_audited.csv'))
parser.add_argument('--output-dir', type=pathlib.Path, required=True)
args = parser.parse_args()
ROOT = args.evidence_dir
args.output_dir.mkdir(parents=True, exist_ok=True)
with args.checkpoint.open(newline='', encoding='utf-8') as fp: old = list(csv.DictReader(fp))
with args.baseline.open(newline='', encoding='utf-8') as fp: allrows = list(csv.DictReader(fp))
assert old==allrows[:83], 'Historical rows modified'
ANSI = re.compile(r'\x1b\[[0-9;]*m')
def parse_test(s, instance, text):
    t = ANSI.sub('', text).replace('\r', '\n')
    b = t.split("'>>>>> Start Test Output'")[-1].split("'>>>>> End Test Output'")[0]
    if instance.startswith('django__'):
        counts = re.findall('(?m)^Ran (\\d+) tests? in [^\\n]+', b)
        oks = re.findall('(?m)^(OK(?: \\(skipped=(\\d+)\\))?|FAILED \\(([^\\n]+)\\))$', b)
        assert counts and oks, (instance, counts, oks, b[-1500:])
        total = int(counts[-1])
        summary, skipped_text, failed_text = oks[-1]
        skipped = int(skipped_text or 0)
        failure = int((re.search('failures=(\\d+)', failed_text or '') or [None, '0'])[1])
        errors = int((re.search('errors=(\\d+)', failed_text or '') or [None, '0'])[1])
        failed = failure + errors
        passed = total - failed - skipped
        assert passed >= 0, (instance, total, failed, skipped)
        return {'runner': 'django_unittest', 'total': total, 'passed': passed, 'failed': failed, 'skipped': skipped, 'errors': errors, 'summary': summary, 'nested_expected_skips': 0}
    if instance.startswith('sympy__'):
        summaries = re.findall('tests finished: ([^\\n]+)', b)
        assert summaries, (instance, b[-1500:])
        summ = summaries[-1]

        def val(key):
            m = re.search('(\\d+) ' + key, summ)
            return int(m.group(1)) if m else 0
        passed = val('passed')
        failed = val('failed')
        exceptions = val('exceptions?')
        skipped = val('skipped')
        return {'runner': 'sympy_bin_test', 'total': passed + failed + exceptions + skipped, 'passed': passed, 'failed': failed + exceptions, 'skipped': skipped, 'errors': exceptions, 'summary': 'tests finished: ' + summ, 'nested_expected_skips': 0}
    summaries = re.findall('(?m)^\\s*[=]{2,}\\s*([^\\n]*?\\b(?:passed|failed|skipped|errors?)\\b[^\\n]*?)\\s*[=]{2,}\\s*$', b)
    assert summaries, (instance, b[-2200:])
    summary = summaries[-1].strip()

    def val(key):
        m = re.search('(\\d+) ' + key, summary)
        return int(m.group(1)) if m else 0
    passed = val('passed')
    failed = val('failed') + val('errors')
    skipped = val('skipped')
    xfailed = val('xfailed')
    xpassed = val('xpassed')
    nested = re.findall('(?m)^\\s*[=]{2,}\\s*([^\\n]*?\\bskipped\\b[^\\n]*?)\\s*[=]{2,}\\s*$', b)
    nested_expected = sum((int(m.group(1)) for tline in nested if (m := re.search('(\\d+) skipped', tline)))) - val('skipped')
    if instance.startswith('sphinx-doc__'):
        assert re.search('(?m)^\\s*py39: exit 0 ', b), instance
        assert 'congratulations :)' in b, instance
    return {'runner': 'tox_pytest' if instance.startswith('sphinx-doc__') else 'pytest', 'total': passed + failed + skipped + xfailed + xpassed, 'passed': passed, 'failed': failed, 'skipped': skipped, 'errors': val('errors'), 'summary': summary, 'nested_expected_skips': nested_expected}

run_errors=[];data=[]
def ztext(z,suff):
    xs=[p for p in z.namelist() if p.endswith(suff)]
    if len(xs)!=1:raise ValueError(f'{suff}: found {xs}')
    return z.read(xs[0]).decode('utf8','replace')
def filelist(patch):return re.findall(r'(?m)^diff --git a/([^\n]+?) b/([^\n]+)$',patch)
def diff_extract(log,part):
    if part=='before': s=log.split('Git diff before:',1)[1].split(' - INFO - Test output for ',1)[0]
    else:s=log.split('Git diff after:',1)[1].split(' - INFO - Grading answer',1)[0]
    s=re.split(r'\n20\d{2}-\d\d-\d\d \d\d:\d\d:\d\d[,\.]\d+',s,maxsplit=1)[0]
    return '\n'.join(line.rstrip() for line in s.strip().splitlines()).strip()

def check(s,i,prior):
    with zipfile.ZipFile(ROOT/f'sweabs-result-{s}-{i}.zip') as z:
        if z.testzip() is not None:raise AssertionError('corrupt ZIP')
        r=json.loads(z.read('result.json'));m=json.loads(z.read('metadata.json'))
        t=json.loads(z.read('abs_instance.json'))[0];pred=json.loads(z.read('one_prediction.jsonl'))
        patch=ztext(z,'/patch.diff').encode();log=ztext(z,'/run_instance.log');test=ztext(z,'/test_output.txt');ev=ztext(z,'/eval.sh')
        rep=json.loads(ztext(z,'/report.json'));rep=next(iter(rep.values()))
        datarev={r['dataset_revision'],m['dataset_revision']};testrev={r['test_dataset_revision'],m['test_dataset_revision']}
        claims={
           'same_id':r['instance_id']==m['instance_id']==pred['instance_id']==t['instance_id']==prior['instance_id'],
           'same_sample':r['sample']==s==m['sample'],
           'hash_patch':r['patch_sha256']==m['patch_sha256']==hashlib.sha256(pred['model_patch'].encode()).hexdigest()==hashlib.sha256(patch).hexdigest()==prior['patch_sha256'],
           'hash_test':r['test_patch_sha256']==m['test_patch_sha256']==hashlib.sha256(t['test_patch'].encode()).hexdigest(),
           'base':r['base_commit']==m['base_commit']==t['base_commit'],
           'rev':len(datarev)==len(testrev)==1,
           'original_resolved':r['original_resolved'] is True and m['original_resolved'] is True,
           'pinned_harness':r['sweabs_commit']==m['sweabs_commit']=='26b4c736ca3d566d8395d7999304d0264abe7992',
           'base_marker':f'PREPATCH_BASE_COMMIT_VERIFIED: {r["base_commit"]}' in log,
           'patch_report':rep['patch_is_None'] is False and rep['patch_exists'] is True and rep['patch_successfully_applied'] is True,
           'test_patch_in_eval':t['test_patch'] in ev,
           'test_patch_command':'+ git apply -v -' in test,
           'test_marker':"'>>>>> Start Test Output'" in test and "'>>>>> End Test Output'" in test,
           'run_id':r['run_id']==prior['run_id']==f'pilot_{r["run_id"].split("_")[1]}_1_{s}_{i}',
           'base_check':r.get('base_commit_check')=='VERIFIED'
        }
        bf=diff_extract(log,'before');af=diff_extract(log,'after');
        bpaths=[a for a,b in filelist(bf)];apaths=[a for a,b in filelist(af)]
        tpaths=[b for a,b in filelist(t['test_patch'])];mpaths=[b for a,b in filelist(pred['model_patch'])];
        claims['prior_commit_active']=bool(bpaths) and bool(set(bpaths).intersection(set(mpaths)))
        claims['test_patch_applied']=bool(tpaths) and all(f'Applied patch {p} cleanly.' in test for p in tpaths)
        diff_equal=bf==af
        overlap=set(bpaths)-set(apaths)
        if not diff_equal and not (overlap and overlap.issubset(set(tpaths)) and set(apaths).issubset(set(bpaths))):
            raise ValueError(f'unexpected repository diff change: before {bpaths}, after {apaths}')
        # Whether entire original model repo modifications survived the test process
        claims['patch_preserved']=diff_equal
        stats=parse_test(s,r['instance_id'],test)
        if not diff_equal:outcome='UNVERIFIED';reason='model_repo_diff_changed_after_test'
        elif stats['failed']>0:outcome='FAIL';reason='augmented_assertion_failure_or_exception'
        elif stats['skipped']>0:outcome='UNVERIFIED';reason='augmented_tests_skipped'
        elif stats['total']>0 and stats['passed']>0:outcome='PASS';reason='all_augmented_tests_executed_pass'
        else:outcome='UNVERIFIED';reason='ambiguous_test_runner'
        failed=[key for key,val in claims.items() if not val]
        if failed and failed!=['patch_preserved']:
            outcome='UNVERIFIED';reason='identity_or_artifact_checks_failed:'+','.join(failed)
        # A previously flagged 884 KB generated/build patch has no full-diff verification.
        # Passing 15 executed tests does not establish the exact complete patch identity.
        if r.get('patch_diff_check')=='NOT_CHECKED' and any(path.startswith('build/lib/') for path in mpaths):
            outcome='UNVERIFIED';reason='full_model_patch_diff_unverified_generated_build_files'
        if s==2 and i==4 and r.get('patch_diff_check')=='NOT_CHECKED':
            # Historical manual review verified the relevant django/core/validators.py
            # repository diff; the unmatched auxiliary patch file was AGENTS.md.
            assert 'django/core/validators.py' in bpaths
            assert set(mpaths)-set(bpaths) <= {'AGENTS.md'} | {p for p in mpaths if p.startswith('workspace/')}
            if stats['failed'] > 0 and not failed:
                outcome='FAIL'; reason='augmented_assertions_failed_manual_source_diff_verified'

        return dict(sample=s,offset=i,instance_id=r['instance_id'],prior=prior['outcome'],collector=r['outcome'],candidate=outcome,reason=reason,run_id=r['run_id'],repo_diff_equal=diff_equal,repo_diff_drop=';'.join(sorted(overlap)),model_files=';'.join(sorted(set(mpaths).intersection(set(bpaths)))),augmented_files=';'.join(tpaths),passed=stats['passed'],failed=stats['failed'],skipped=stats['skipped'],runner=stats['runner'],collector_diff_check=r.get('patch_diff_check',''),test_files_applied=claims.get('test_patch_applied'),patch_identity_verified=all(v for k,v in claims.items() if k!='patch_preserved'),summary=stats['summary'],nested_skips=stats['nested_expected_skips'],checks_failed=';'.join(failed),evidence_url=f'https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/{r["run_id"].split("_")[1]}',sha=r['patch_sha256'])

for row in old:
 s,i=int(row['sample']),int(row['offset'])
 try: data.append(check(s,i,row))
 except Exception as e:
  run_errors.append((s,i,row['instance_id'],type(e).__name__,str(e)[:700]));
  data.append(dict(sample=s,offset=i,instance_id=row['instance_id'],prior=row['outcome'],collector='',candidate='UNVERIFIED',reason='REVIEW_REQUIRED: '+str(e)[:240],checks_failed='exception'))

if run_errors:
    raise RuntimeError(f'83-run re-audit is incomplete; no outputs written: {run_errors}')
assert len(data)==83
original_counter=collections.Counter(row['outcome'] for row in old)
revised_counter=collections.Counter(row['candidate'] for row in data)
corrections=[]
for aud, orig in zip(data, old):
    if aud['candidate']!=orig['outcome']:
        corrections.append({'sample':orig['sample'], 'offset':orig['offset'],
            'instance_id':orig['instance_id'], 'patch_sha256':orig['patch_sha256'],
            'run_id':orig['run_id'], 'original_outcome':orig['outcome'],
            'revised_outcome':aud['candidate'],'reason':aud['reason'],
            'raw_summary':aud['summary'],'passed':aud['passed'], 'failed':aud['failed'],
            'skipped':aud['skipped'], 'lost_model_patch_files':aud['repo_diff_drop'],
            'evidence_url':aud['evidence_url']})
revised=[dict(row) for row in allrows]
for idx,aud in enumerate(data):
    if aud['candidate']!=revised[idx]['outcome']:
        revised[idx]['outcome']=aud['candidate']
        revised[idx]['source']='historical_rawlog_reaudit_2026-11-12'
        revised[idx]['note']=f"CORRECTION {aud['prior']} -> {aud['candidate']}; {aud['reason']}; earlier raw result {aud['summary']}; exact-patch integrity issue: {aud['repo_diff_drop']}"
        revised[idx]['method_count']=str(aud['passed']+aud['failed']+aud['skipped'])
        revised[idx]['passed']=str(aud['passed'])
        revised[idx]['failed']=str(aud['failed'])
        revised[idx]['skipped']=str(aud['skipped'])
assert len(revised)==198
out_dir=args.output_dir
for name,rows,fields in [
    ('sweabs_historical_83_reaudit_evidence.csv',data,list(data[0])),
    ('sweabs_historical_83_corrections.csv',corrections,list(corrections[0]) if corrections else ['sample','offset','instance_id','original_outcome','revised_outcome','reason']),
    ('sweabs_full_198_cumulative_v2.csv',revised,list(revised[0])),
]:
    with (out_dir/name).open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
print('historic rows:',len(old),'original:',dict(original_counter),'revised:',dict(revised_counter))
print('corrections:',corrections)
print('whole revised:',dict(collections.Counter(row['outcome'] for row in revised)))
print('outputs:',out_dir)
