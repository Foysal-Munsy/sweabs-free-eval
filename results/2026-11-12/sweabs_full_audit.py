#!/usr/bin/env python3
"""Offline evidence audit: frozen SWE-ABS sampled evaluations, no test reruns.

Uses only original archived GitHub Actions evidence and the existing 83-row CSV.
Never conflates the upstream harness resolved flag with augmented test verdicts.
"""
import csv, hashlib, json, re, zipfile, collections
from pathlib import Path

ROOT=Path('/mnt/data')
EXISTING=ROOT/'sweabs_samples1_2_first83_cumulative.csv'
TODAY='2026-11-12'
ANSI=re.compile(r'\x1b\[[0-9;]*m')
RUNIDS={
    (2,20):43181184322,(2,30):43181332699,(2,40):43181336920,(2,50):43181340403,(2,60):43181346009,
    (3,0):43182603318,(3,10):43182697559,(3,20):43182701126,(3,30):43182706543,(3,40):43182715959,(3,50):43182719908,(3,60):43182738449,
}

def getrun(s,o):return RUNIDS[(s,(o//10)*10)]
def shas(x):return hashlib.sha256(x).hexdigest()
def zfile(z,end):
    arr=[x for x in z.namelist() if x.endswith(end)]
    assert len(arr)==1,(end,arr)
    return z.read(arr[0]).decode('utf8','replace')
def difffiles(patch):return [b for a,b in re.findall(r'^diff --git a/(.*?) b/(.*?)$',patch,re.M)]
def result_report(z):
    o=json.loads(zfile(z,'/report.json'))
    assert len(o)==1,o.keys()
    return next(iter(o.values()))

def parse_test(s,instance,text):
    t=ANSI.sub('',text).replace('\r','\n')
    b=t.split("'>>>>> Start Test Output'")[-1].split("'>>>>> End Test Output'")[0]
    # Strict final harness result; nested pytester subprocesses can have earlier skipped/failed fragments.
    if instance.startswith('django__'):
        counts=re.findall(r'(?m)^Ran (\d+) tests? in [^\n]+',b)
        oks=re.findall(r'(?m)^(OK(?: \(skipped=(\d+)\))?|FAILED \(([^\n]+)\))$',b)
        assert counts and oks,(instance, counts, oks, b[-1500:])
        total=int(counts[-1]); summary,skipped_text,failed_text=oks[-1]
        skipped=int(skipped_text or 0)
        failure=int((re.search(r'failures=(\d+)',failed_text or '') or [None,'0'])[1]);errors=int((re.search(r'errors=(\d+)',failed_text or '') or [None,'0'])[1])
        failed=failure+errors
        passed=total-failed-skipped
        assert passed>=0,(instance,total,failed,skipped)
        return {'runner':'django_unittest','total':total,'passed':passed,'failed':failed,'skipped':skipped,'errors':errors,'summary':summary,'nested_expected_skips':0}
    if instance.startswith('sympy__'):
        summaries=re.findall(r'tests finished: ([^\n]+)',b)
        assert summaries,(instance,b[-1500:])
        summ=summaries[-1]
        def val(key):
            m=re.search(r'(\d+) '+key,summ)
            return int(m.group(1)) if m else 0
        passed=val('passed');failed=val('failed');exceptions=val('exceptions?');skipped=val('skipped')
        return {'runner':'sympy_bin_test','total':passed+failed+exceptions+skipped,'passed':passed,'failed':failed+exceptions,'skipped':skipped,'errors':exceptions,'summary':'tests finished: '+summ,'nested_expected_skips':0}
    # pytest, pytester, tox-wrapped pytest
    summaries=re.findall(r'(?m)^\s*[=]{2,}\s*([^\n]*?\b(?:passed|failed|skipped|errors?)\b[^\n]*?)\s*[=]{2,}\s*$',b)
    assert summaries,(instance,b[-2200:])
    summary=summaries[-1].strip()
    def val(key):
        m=re.search(r'(\d+) '+key,summary)
        return int(m.group(1)) if m else 0
    passed=val('passed');failed=val('failed')+val('errors');skipped=val('skipped')
    xfailed=val('xfailed');xpassed=val('xpassed')
    # nested subprocess results are not skipped tests in the outer augmented tests.
    nested=re.findall(r'(?m)^\s*[=]{2,}\s*([^\n]*?\bskipped\b[^\n]*?)\s*[=]{2,}\s*$',b)
    nested_expected=sum(int(m.group(1)) for tline in nested if (m:=re.search(r'(\d+) skipped',tline))) - val('skipped')
    if instance.startswith('sphinx-doc__'):
        assert re.search(r'(?m)^\s*py39: exit 0 ',b),instance
        assert 'congratulations :)' in b,instance
    return {'runner':'tox_pytest' if instance.startswith('sphinx-doc__') else 'pytest','total':passed+failed+skipped+xfailed+xpassed,'passed':passed,'failed':failed,'skipped':skipped,'errors':val('errors'),'summary':summary,'nested_expected_skips':nested_expected}

with EXISTING.open(newline='',encoding='utf8') as f:
    reader=csv.DictReader(f); original=list(reader);fields=reader.fieldnames
assert len(original)==83
assert [(int(r['sample']),int(r['offset'])) for r in original[:63]]==[(1,i) for i in range(63)]
assert [(int(r['sample']),int(r['offset'])) for r in original[63:]]==[(2,i) for i in range(20)]
new=[];details=[];errors=[];update_counts=collections.Counter()
for s,lo,hi in ((2,20,68),(3,0,67)):
    for i in range(lo,hi):
        path=ROOT/f'sweabs-result-{s}-{i}.zip'
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None,path
            r=json.loads(z.read('result.json'));meta=json.loads(z.read('metadata.json'))
            instdata=json.loads(z.read('abs_instance.json'))
            assert isinstance(instdata,list) and len(instdata)==1
            task=instdata[0]
            pred=json.loads(z.read('one_prediction.jsonl').decode('utf8').strip())
            report=result_report(z)
            log=zfile(z,'/run_instance.log')
            test=zfile(z,'/test_output.txt')
            evalsh=zfile(z,'/eval.sh')
            patch=zfile(z,'/patch.diff').encode('utf8')
            assert r['sample']==s and r['instance_id']==meta['instance_id']==task['instance_id']==pred['instance_id'],(s,i,'identity')
            assert r['original_resolved'] is True and meta['original_resolved'] is True,(s,i,'original')
            assert r['model_name_or_path']==f'openhands-gemini3-flash-sample-{s}',(s,i,'model')
            assert r['dataset_revision']==meta['dataset_revision'],(s,i,'dataset_revision')
            assert r['test_dataset_revision']==meta['test_dataset_revision'],(s,i,'test_dataset_revision')
            assert r['base_commit']==meta['base_commit']==task['base_commit'],(s,i,'base')
            assert r['patch_sha256']==meta['patch_sha256']==shas(patch)==shas(pred['model_patch'].encode('utf8')),(s,i,'patch hash')
            assert r['test_patch_sha256']==meta['test_patch_sha256']==shas(task['test_patch'].encode('utf8')),(s,i,'test hash')
            assert r['run_id']==f'pilot_{getrun(s,i)}_1_{s}_{i}',(s,i,'run id')
            assert f'PREPATCH_BASE_COMMIT_VERIFIED: {r["base_commit"]}' in log,(s,i,'prepatch')
            assert report['patch_is_None'] is False and report['patch_exists'] is True and report['patch_successfully_applied'] is True,(s,i,'report patch')
            assert r['base_commit_check']=='VERIFIED',(s,i,'base check')
            assert r['sweabs_commit']==meta['sweabs_commit']=='26b4c736ca3d566d8395d7999304d0264abe7992',(s,i,'sweabs SHA')
            target_paths=difffiles(task['test_patch'])
            assert target_paths,(s,i,'test patch target')
            assert task['test_patch'] in evalsh,(s,i,'test patch script exact')
            assert '+ git apply -v -' in test,(s,i,'test patch command')
            assert all(f'Applied patch {p} cleanly.' in test for p in target_paths),(s,i,'augmented file patch absent')
            assert "'>>>>> Start Test Output'" in test and "'>>>>> End Test Output'" in test,(s,i,'test bounds')
            if r.get('augmented_test_patch_check') is not None:
                assert r['augmented_test_patch_check']=='ALL_EXPECTED_FILES_APPLIED',(s,i,'test check')
            before=log.split('Git diff before:',1)[-1].split(' - INFO - Test output for ',1)[0]
            after=log.split('Git diff after:',1)[-1].split(' - INFO - Grading answer',1)[0]
            before_files=re.findall(r'^diff --git a/([^ ]+) b/[^\n]+',before,re.M)
            after_files=re.findall(r'^diff --git a/([^ ]+) b/[^\n]+',after,re.M)
            assert before_files,(s,i,'no initial repo diff')
            # Exact before/after repository diffs are required, not just matching file lists.
            def normalized_repo_diff(segment):
                segment=segment.split('2026-11-12',1)[0]
                return '\n'.join(line.rstrip() for line in segment.strip().splitlines()).strip()
            repo_diff_equal=normalized_repo_diff(before)==normalized_repo_diff(after)
            overlap=set(before_files)-set(after_files)
            assert repo_diff_equal or (overlap and overlap.issubset(set(target_paths)) and set(after_files).issubset(set(before_files))), (s,i,'unexpected model repository diff loss',before_files,after_files)
            assert not repo_diff_equal or before_files==after_files,(s,i,'inconsistent diff')
            # Collector could not inspect full repo diff in 4 runs due extra workspace files;
            # inspect the relevant before/after repo file diffs instead.
            expected_repo_files=[x for x in difffiles(patch.decode('utf8','replace')) if not x.startswith(('workspace/','AGENTS.md','build/lib/'))]
            assert set(before_files).intersection(expected_repo_files),(s,i,'patch not active repo diff',before_files,expected_repo_files)
            stats=parse_test(s,r['instance_id'],test)
            if not repo_diff_equal:
                outcome='UNVERIFIED'
                kind='model_patch_partially_reverted_by_overlapping_augmented_test_file_cleanup'
            elif stats['failed']>0:
                outcome='FAIL'
                kind='assertion_failure_or_test_exception'
            elif stats['skipped']>0:
                outcome='UNVERIFIED'
                kind='augmented_test_skips_or_partial_coverage'
            elif stats['total']>0 and stats['passed']>0:
                outcome='PASS'
                kind='all_executed_augmented_tests_passed'
            else:
                outcome='UNVERIFIED'
                kind='no_confirmed_augmented_test_result'
            if r['outcome']!=outcome: update_counts[(r['outcome'],outcome)]+=1
            model_check=r['patch_diff_check']
            if model_check!='REPOSITORY_CHANGE_LINES_MATCH':
                assert model_check=='NOT_CHECKED',(s,i,model_check)
                kind+='; repository_delta_inferred_from_diff_before_after_not_exact'
            core=f"{stats['runner']}: {stats['total']} augmented tests; {stats['passed']} passed, {stats['failed']} failed/errors, {stats['skipped']} skipped."
            note=core+' Base commit, frozen model/test patch SHA, per-run identity, and test-patch application verified. '+('Model repo diff unchanged across test execution. ' if repo_diff_equal else 'Model repo diff changed during test execution. ')
            if stats['runner']=='tox_pytest':note+='tox py39 exit 0 confirmed. '
            if stats['nested_expected_skips']>0:note+=f"Nested pytester subprocess contained {stats['nested_expected_skips']} intentional skips; outer augmented suite passed. "
            if stats['failed']>0:
                if repo_diff_equal:
                    note+='Observed augmented-test assertion(s) or functional exception(s); provisional FAIL pending independent test-validity review. '
                else:
                    note+='Observed augmented test failure(s), but exact model-patch identity was compromised; do not assign definitive augmented FAIL. '
                if stats['skipped']>0:note+='Some augmented tests were skipped; FAIL would also have incomplete coverage. '
            elif stats['skipped']>0:
                note+='Augmented tests skipped (e.g., backend support); partial coverage; retain UNVERIFIED. '
            else:note+='No failures, runner errors, or skipped outer augmented tests. '
            if not repo_diff_equal:note+=f'Identity limitation: model patch also modified augmented test file(s) {sorted(overlap)}. Test script checked out those paths before applying augmented tests, so exact original model-patch state did not persist through the augmented test; mark UNVERIFIED regardless of observed runner result. '
            if model_check=='NOT_CHECKED':note+='Collector exact repository-diff match unavailable for this patch format; complete raw before/after active repository diff equivalence and successful patch application checked. '
            if r['reason']=='augmented_test_file_manifest_missing':note+='Collector missed in-place test-file augmentation; raw git apply and test execution confirmed. '
            if r['reason']!='verified_augmented_test_runner_with_base_and_repository_patch':note+=f"Collector reason: {r['reason']}. "
            if stats['failed']>0 and stats['errors']>0:note+=f"{stats['errors']} failure(s) were test-level exceptions, not harness infrastructure errors. "
            note+=f"Raw evidence: https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/{getrun(s,i)}"
            new.append(dict(sample=str(s),offset=str(i),instance_id=r['instance_id'],outcome=outcome,source=f'github_raw_per_patch_reaudit_{TODAY}',method_count=str(stats['total']),passed=str(stats['passed']),failed=str(stats['failed']),skipped=str(stats['skipped']),patch_sha256=r['patch_sha256'],run_id=r['run_id'],note=note))
            details.append(dict(sample=s,offset=i,instance_id=r['instance_id'],github_run_id=getrun(s,i),github_run_url=f'https://github.com/Foysal-Munsy/sweabs-free-eval/actions/runs/{getrun(s,i)}',archived_zip=path.name,original_resolved=r['original_resolved'],collector_outcome=r['outcome'],audited_outcome=outcome,outcome_reason=kind,runner=stats['runner'],augmented_count=stats['total'],augmented_pass=stats['passed'],augmented_fail_or_errors=stats['failed'],augmented_test_errors=stats['errors'],augmented_skipped=stats['skipped'],nested_expected_skips=stats['nested_expected_skips'],last_runner_summary=stats['summary'],frozen_dataset_revision=r['dataset_revision'],frozen_abs_revision=r['test_dataset_revision'],frozen_sweabs_sha=r['sweabs_commit'],patch_sha256=r['patch_sha256'],test_patch_sha256=r['test_patch_sha256'],base_commit=r['base_commit'],base_check=r['base_commit_check'],patch_hash_verified=True,model_patch_application_verified=repo_diff_equal,repo_diff_before_after_files_match=repo_diff_equal,collector_diff_check=model_check,test_patch_hash_verified=True,test_patch_files_applied=True,augmented_test_files=';'.join(target_paths),collector_reason=r['reason'],note=note))

assert len(new)==115 and len(details)==115
combined=original+new
assert len(combined)==198
ids=[(int(x['sample']),int(x['offset'])) for x in combined]
assert len(set(ids))==198
assert set(ids)=={(1,i) for i in range(63)}|{(2,i) for i in range(68)}|{(3,i) for i in range(67)}
assert combined[:83]==original
new.sort(key=lambda r:(int(r['sample']),int(r['offset'])))
combined=original+new
finalcsv=ROOT/'sweabs_full_198_cumulative_audited.csv'
with finalcsv.open('w',newline='',encoding='utf8') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(combined)
evidencecsv=ROOT/'sweabs_samples2_3_full_audit_evidence_115.csv'
with evidencecsv.open('w',newline='',encoding='utf8') as f:
 writer=csv.DictWriter(f,fieldnames=list(details[0]));writer.writeheader();writer.writerows(details)
counts=collections.Counter(x['outcome'] for x in combined)
per_sample={s:collections.Counter(x['outcome'] for x in combined if x['sample']==str(s)) for s in (1,2,3)}
print('total',len(combined),counts)
print('per_sample',per_sample)
print('collector_changes',dict(update_counts))
print('not_checked',[(x['sample'],x['offset'],x['instance_id'],x['audited_outcome']) for x in details if x['collector_diff_check']=='NOT_CHECKED'])
print('notes',[(x['sample'],x['offset'],x['instance_id']) for x in details if x['audited_outcome']=='UNVERIFIED'])
print('files',finalcsv,evidencecsv)
