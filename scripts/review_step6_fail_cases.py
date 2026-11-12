#!/usr/bin/env python3
"""Step 6: reproducible *documentary* semantic review of provisional FAIL records.

Inputs: archived v2 outcome CSV and original raw per-patch evidence ZIPs.
Does not execute model code or alter the v2 labels. The manually authored
review rationale is kept separately below rather than inferred from tests.
"""
from pathlib import Path
from collections import Counter, defaultdict
from hashlib import sha256
import csv, zipfile, json, re, textwrap

ROOT=Path('/mnt/data')
SRC=ROOT/'step5_outputs/sweabs_full_198_cumulative_v2.csv'
OUT=ROOT/'step6_outputs'
OUT.mkdir(exist_ok=True)
REPO='https://github.com/Foysal-Munsy/sweabs-free-eval'
RFC7231='https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1'
RFC3986='https://www.rfc-editor.org/rfc/rfc3986.html#section-3.2.1'
RFC1738='https://www.rfc-editor.org/rfc/rfc1738.html#section-3.1'
PYDOC='https://docs.python.org/3/library/functions.html#staticmethod'

# Each task rationale reviewed against ORIGINAL problem statement in the archived
# ABS record, original merged PR description, enhanced test_patch, and raw test log.
# Supported does NOT mean independently reproduced or finalized semantic correctness.
REVIEW={
'django__django-10097': dict(status='unresolved',scope='Directly referenced by historical PR; newer URI standard conflicts',
  assertion='Unencoded second colon in userinfo password must be invalid URL; failures http://foo:bar:baz@example.com and IPv6 user:pa:ss.',
  reason='The 2018 Django PR explicitly required encoding unescaped colons in user/password under RFC1738. But RFC3986 section 3.2.1 permits colon in generic URI userinfo; Django URLValidator policy across standards and backwards compatibility is not independently established. The two observed failures do not establish universally invalid URLs.',
  alternative='The historical Django URLValidator behavior can intentionally use the stricter RFC1738 policy; if evaluated against that specific policy these assertions may be defensible.',
  next='Retrieve contemporaneous Django validator tests / maintainer policy for extra password colons and record which standard is binding.',docs=(RFC1738,RFC3986)),
'django__django-11206': dict(status='unresolved',scope='Issue covers small decimals; failing additions target negative signed zero',
  assertion='Negative tiny Decimal values whose magnitude falls below display resolution must print 0.00 rather than -0.00.',
  reason='The original bug concerns avoiding scientific notation for tiny Decimal values; the failed assertions depend solely on stripping a negative sign from rounded zero. The issue does not specify signed-zero policy, and the observed format -0.00 still avoids scientific notation.',
  alternative='The reference fix coerces too-small values to Decimal(0), which produces positive zero. That makes the tightened expectation consistent with the reference implementation but not necessarily the issue specification.',
  next='Check Django documented negative-number rounding behavior and maintainer discussion; decide whether negative-zero normalization is a requirement.',docs=()),
'django__django-11848': dict(status='invalid_test',scope='RFC850 dynamic two-digit year: one contradictory century-wrap assertion',
  assertion='When current year is 2099, RFC850 date 01-Jan-00 must be interpreted as 2000 (test expectation).',
  reason='RFC7231 says map to a past century only if candidate timestamp appears MORE THAN 50 years in future. Relative to July 2099, January 2100 is less than one year ahead, so 2100 is the correct interpretation, not 2000. The raw failure is exactly 2100 (actual) versus 2000 (expected). This strengthened assertion is objectively inconsistent with its cited rule.',
  alternative='The test author likely assumed 2-digit 00 always represents year 2000 at the 2099 boundary, overlooking current-century rollover.',
  next='Exclude this failing assertion as invalid; do not treat this run as a validated semantic failure absent another sound failing assertion.',docs=(RFC7231,)),
'django__django-11999': dict(status='valid_failure',scope='Inherited get_FIELD_display override follows core issue',
  assertion='A get_phase_display override inherited from a mixin must be honored instead of regenerated choice display.',
  reason='Original bug and merged PR require preserving custom get_FIELD_display methods. The added mixin supplies that method before models.Model in MRO; raw run returns generated choice label One instead of mixin-override. The expected method-resolution behavior is directly consistent with the PR goal.',
  alternative='The original example used an inline model method, not an inherited mixin. Inherited overrides are a reasonable extension but deserve a maintainer check.',
  next='Retain as review-supported provisional FAIL; verify mixin precedence against the affected Django version before finalization.',docs=()),
'django__django-12273': dict(status='unresolved',scope='Enhanced check changes PK to a non-None integer, original issue is pk=None',
  assertion='Setting Congressman.pk to old_pk+7 must immediately update politician_id parent-link field.',
  reason='Original issue and merged PR are about copying multi-table inheritance records by assigning pk=None. The failing enhanced assertion instead assigns a new non-None primary key and assumes immediate parent-link propagation, a separate mutation whose persistence semantics are not established from the issue.',
  alternative='The reference implementation updates parent links for any pk value; keeping internal IDs consistent can be a general invariant, though it is stronger than the documented copy operation.',
  next='Review Django multi-table inheritance PK documentation and test whether non-None assignment is a supported API guarantee.',docs=()),
'django__django-12304': dict(status='unresolved',scope='Subclass deliberately overrides the new template-safety flag',
  assertion='Even if subclass defines do_not_call_in_templates=False, Choices metaclass must force it True or error.',
  reason='Issue requires enum choice classes to be template-usable by default. The failing strengthened test asserts an extra policy for subclasses that explicitly override the flag, which the issue does not establish. It may conflict with customizable class attributes.',
  alternative='If do_not_call_in_templates is a non-overridable invariant, enforcing True in the metaclass is a defensible implementation (the reference patch does so).',
  next='Check Django template flag override contract; separate guaranteed default behavior from forced subclass behavior.',docs=()),
'django__django-14311': dict(status='valid_failure',scope='One direct non-package -m restart failure; second synthetic __main__ case',
  assertion='get_child_arguments must preserve -m singlemodule when __spec__.name is singlemodule; synthetic __main__ with parent should use its parent.',
  reason='The issue is specifically about preserving python -m module identities on autoreload. The raw tests observe fallback to script execution for a single-module spec, which is inconsistent with the -m restart purpose. The additional mocked top-level __main__ spec may not arise naturally.',
  alternative='A synthetic spec.name="__main__", parent="top_level_pkg" might be unrealistic; do not rely on that subtest alone. The singlemodule assertion is sufficient documentary support for the broader behavior.',
  next='Retain review-supported provisional FAIL; independently validate the singlemodule invocation path in an actual Python -m scenario.',docs=()),
'django__django-14999': dict(status='valid_failure',scope='No-op RenameModel with unchanged explicit db_table and FK/M2M',
  assertion='When explicit db_table remains unchanged on model rename, database_forwards should execute no schema queries despite FK/M2M relations.',
  reason='Merged PR explicitly makes RenameModel a noop when db_table does not change. Sample 1 raw run executes seven schema queries rebuilding a related M2M table, contradicting that target behavior. This failure is directly tied to the original bug.',
  alternative='On some DB backends relation-column metadata may require schema work even when table name remains; SQL effect needs independent backend review.',
  next='Retain sample-1 case as review-supported, verify emitted SQL semantics and whether relation-column names should change.',docs=()),
'django__django-15252': dict(status='unresolved',scope='Test pins internal method call in an empty-plan migration',
  assertion='MigrationExecutor._create_project_state must be called with with_applied_migrations=False if plan=[] and migrations table missing.',
  reason='The PR aims to prevent creation of django_migrations table when there are no migrations to apply. Raw failure is solely an internal mocked call argument (True rather than False); the test does not demonstrate that forbidden table creation occurred or that returned state is incorrect.',
  alternative='The reference implementation uses False to avoid implying applied migrations where the table is absent; that internal contract might be necessary for correctness.',
  next='Add observable DB schema/state assertions in a genuine multi-database scenario; do not over-interpret the mock-call failure.',docs=()),
'django__django-15916': dict(status='environment_sensitive',scope='Test fixture passes a Python-3.9 noncallable staticmethod descriptor as callback',
  assertion='A class-level staticmethod callback must be ignored in favor of Meta.formfield_callback; ModelForm construction must not raise TypeError.',
  reason='Two added tests define formfield_callback=staticmethod(class_callback). Under the actual Python 3.9 runner, raw errors arise at class construction because the descriptor is not a callable. Python documents that staticmethod objects themselves became callable only in 3.10. The PR also intended support for both class-level and Meta variants, so callback precedence is not conclusively specified.',
  alternative='The test could be intended to guarantee Meta precedence even when class-level callback is not callable. But the Python-version-dependent descriptor makes its semantics and portability uncertain.',
  next='Repeat targeted tests with an ordinary callable class attribute and use runtime-version-matched Python semantics; decide precedence from merged PR tests.',docs=(PYDOC,)),
'django__django-16661': dict(status='unresolved',scope='Negative security/allowlist invariant beyond original allowed deep lookup',
  assertion='A bare related lookup not explicitly included in list_filter must be disallowed even if a subfield path is listed.',
  reason='The source ticket/PR is about incorrectly rejecting an allowed deep related lookup through a OneToOne primary key. The failing extra test instead asserts that prefix relationships must be rejected; Django lookup_allowed can allow some implicit/local-field lookups. The exact allowlist policy for relation prefixes is not established by the issue alone.',
  alternative='Over-broad allowlisting would be a real security regression; an explicit negative test is sensible if it matches Django documented policy.',
  next='Verify default ModelAdmin.lookup_allowed rules and original permitted lookup exceptions for relation prefixes.',docs=()),
'matplotlib__matplotlib-25775': dict(status='valid_failure',scope='Per-Text antialias state propagation and Cairo backend integration',
  assertion='Text.update_from must copy antialiased property, and Cairo GC true antialiasing should yield a mode other than ANTIALIAS_NONE.',
  reason='PR explicitly introduces per-Text/per-Annotation antialias state and targets Agg/Cairo backends. Raw test shows update_from keeps False when copying True, plus Cairo getter remains NONE after setting True. These are relevant violations of its intended per-artist behavior.',
  alternative='Cairo getter modes can differ by backend/library and two SVG comparison tests were skipped; image equivalence and Cairo context semantics need backend-specific confirmation.',
  next='Retain review-supported provisional FAIL; confirm Cairo enum mapping and update_from contract under pinned matplotlib/Cairo versions.',docs=()),
'sympy__sympy-13877': dict(status='invalid_test',scope='Failure is unrelated random_complex_number tolerance keyword, not determinant',
  assertion='random_complex_number(rational=True, tolerance=1e-3) must be supported by random-number utility.',
  reason='Original merged PR and issue concern NaN / zero-pivot behavior in Bareiss determinant. The enhanced failing test instead exercises an optional tolerance kwarg in randtest.random_complex_number; the submitted code may solve pivot detection without adding that unrelated public API. A reference patch touching randtest does not by itself establish it as a necessary external requirement.',
  alternative='The reference implementation added a tolerance option as an auxiliary way to evaluate random rational pivots, so a strict patch-equivalence benchmark might test it; that would conflate implementation detail with task semantics.',
  next='Exclude this failure as out-of-scope for determinant correctness; verify determinant tests directly and retain the original raw observation.',docs=()),
'sympy__sympy-15599': dict(status='valid_failure',scope='Direct required Mod simplification and mathematically valid GCD reduction',
  assertion='Mod(3*k, 2) simplifies to Mod(k, 2); Mod(6*i, 9) equals 3*Mod(2*i, 3) for integer i.',
  reason='The original PR directly targets Mod(3*i,2). The strengthened test fails that exact expression and the gcd reduction identity, with recursion exceptions in two sample runs. These failing equalities follow integer modular arithmetic and are directly related to the issue.',
  alternative='Several other enhanced checks cover general symbolic Mod rearrangements and should be reviewed separately; one passing assertion appears mathematically over-broad for symbolic inputs and should not be used as independent proof of suite-wide soundness.',
  next='Retain review-supported provisional FAIL for direct assertions; independently spot-check all enhanced Mod identities before broader generalization.',docs=()),
'sympy__sympy-24066': dict(status='unresolved',scope='Generic multi-argument Function internal return-shape test beyond exp example',
  assertion='SI._collect_factor_and_dimension(F(dimless_expr, dim_expr)) must return a 3-tuple (factor, dim1, dim2).',
  reason='Issue describes failure to recognize a dimensionless argument of exp in an expression. The failing enhanced test imposes a specific internal output tuple length for an arbitrary symbolic two-argument Function, not the exp RC test. It is consistent with the reference implementation but is not established as a public API contract.',
  alternative='The existing Function branch already returns one dimension per argument, so preserving its established internal shape is reasonable as a regression check even if not part of the original user bug.',
  next='Inspect the pre-patch _collect_factor_and_dimension Function contract and consumer call sites; verify whether 3-tuple is relied upon.',docs=())
}

# Per-run overrides where the failing subtest differs between samples.
OVERRIDE={
('django__django-14999',2):dict(status='unresolved',scope='Case-only db_table rename on SQLite + mocked backend call',
 assertion='When db_table changes from case_tbl to CASE_TBL, schema_editor.alter_db_table must be called in both directions.',
 reason='The failing test asserts a specific internal schema_editor method call on a case-only name change; the original ticket is a no-op for genuinely unchanged explicit names. Case-only naming, SQLite identifier matching, and migration API behavior require backend-specific confirmation. The test explicitly acknowledges SQLite may execute no actual SQL.',
 alternative='The literal table names differ, so treating them as unchanged would be a potentially real error on case-sensitive databases.',
 next='Review Django schema_editor and SQLite/Postgres behavior for case-only renames; avoid treating this test as backend-independent semantic failure.'),
('django__django-14999',3):dict(status='unresolved',scope='Case-only db_table rename on SQLite + mocked backend call',
 assertion='When db_table changes from case_tbl to CASE_TBL, schema_editor.alter_db_table must be called in both directions.',
 reason='The failing test asserts a specific internal schema_editor method call on a case-only name change; the original ticket is a no-op for genuinely unchanged explicit names. Case-only naming, SQLite identifier matching, and migration API behavior require backend-specific confirmation. The test explicitly acknowledges SQLite may execute no actual SQL.',
 alternative='The literal table names differ, so treating them as unchanged would be a potentially real error on case-sensitive databases.',
 next='Review Django schema_editor and SQLite/Postgres behavior for case-only renames; avoid treating this test as backend-independent semantic failure.')
}

rows=list(csv.DictReader(SRC.open(newline='',encoding='utf8')))
assert len(rows)==198
frows=[r for r in rows if r['outcome']=='FAIL']
assert len(frows)==31 and len(set(r['instance_id'] for r in frows))==15
assert set(REVIEW)==set(r['instance_id'] for r in frows)

pids=[]
def failure_names(log):
 # A mixture of Django unittest, pytest and SymPy test runner formats.
 val=[]
 for ln in log.splitlines():
  ln=ln.strip()
  if ln.startswith(('FAIL: ','ERROR: ')):
   val.append(ln.split(' (')[0][:140])
  elif ln.startswith('FAILED ') and '::' in ln:
   val.append(ln[:170])
  elif re.search(r'^\s*sympy/.+:test_\S+',ln):
   val.append(ln[:170])
 if not val:
  val.extend(re.findall(r'(?m)^(test_\w+)\s+(?:F|E)\b',log))
 return ' | '.join(dict.fromkeys(val))[:550]

for r in frows:
 s=int(r['sample']);o=int(r['offset']);task=r['instance_id']
 path=ROOT/f'sweabs-result-{s}-{o}.zip'
 assert path.is_file(),str(path)
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  result=json.loads(z.read('result.json'))
  source=json.loads(z.read('abs_instance.json'))[0]
  p=json.loads(z.read('one_prediction.jsonl'))
  tests=source['test_patch']
  model=p['model_patch']
  assert result['instance_id']==task and p['instance_id']==task
  assert result['sample']==s
  assert result['patch_sha256']==r['patch_sha256']==sha256(model.encode()).hexdigest()
  assert result['test_patch_sha256']==sha256(tests.encode()).hexdigest()
  assert result['base_commit']==source['base_commit']
  basename=next((x for x in z.namelist() if x.endswith('/test_output.txt')),None)
  assert basename
  log=z.read(basename).decode('utf8','replace')
  raw_replay='test_output.txt'
  # Each input task's original PR was independently verified with GitHub REST.
  org,repo_num=task.split('__',1)
  name,num=repo_num.rsplit('-',1)
  repo={'django':'django/django','matplotlib':'matplotlib/matplotlib','sympy':'sympy/sympy'}[org]
  pr=f'https://github.com/{repo}/pull/{num}'
  runid=result['run_id']; match=re.search(r'pilot_(\d+)_',runid);assert match,runid
  runurl=f'{REPO}/actions/runs/{match.group(1)}'
  meta=dict(REVIEW[task]); meta.update(OVERRIDE.get((task,s),{}))
  status=meta['status']
  assert status in {'valid_failure','invalid_test','environment_sensitive','unresolved'}
  test_files=re.findall(r'^diff --git a/(\S+) b/',tests,re.M)
  raw_summary=[]
  for line in log.splitlines():
   if re.search(r'(?m)^(?:FAILED \(failures=|FAILED \(errors=|=+\s*\d+ failed,|=+\s*tests finished:)',line.strip()): raw_summary.append(line.strip())
  rec={
   'sample':s,'offset':o,'instance_id':task,'patch_sha256':r['patch_sha256'],
   'observed_outcome_v2':'FAIL','semantic_review_status':status,
   'review_status_is_final_ground_truth':'NO',
   'pr_url':pr,'source_issue_title':source.get('problem_statement','').splitlines()[0],
   'test_patch_sha256':result['test_patch_sha256'],
   'test_patch_files':' | '.join(test_files),
   'test_patch_in_issue_scope':meta['scope'],
   'failing_assertion':meta['assertion'],
   'observed_failed_subtests':failure_names(log),
   'raw_test_summary':' | '.join(raw_summary[-3:]) or (f"passed={r['passed']} failed={r['failed']}"),
   'review_reason':meta['reason'],
   'opposing_interpretation':meta['alternative'],
   'independent_standard_docs':' | '.join(meta.get('docs',())),
   'next_validation_action':meta['next'],
   'raw_run_url':runurl,
   'archived_result_zip_basename':path.name,
   'run_id':runid,
   'reviewer_method':'AI_assisted_issue_PR_and_augmented_log_review_no_rerun',
   'analysis_recommendation':'do_not_freeze_or_relabel_until_step7'
  }
  pids.append(rec)

pids.sort(key=lambda x:(x['sample'],x['offset']))
cs=Counter(x['semantic_review_status'] for x in pids)
print('review totals',cs)
assert sum(cs.values())==31
# CSV row-level detailed decisions.
cols=list(pids[0])
def writecsv(name,rs,cols):
 with (OUT/name).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=cols,lineterminator='\r\n');w.writeheader();w.writerows(rs)
writecsv('STEP6_FAIL_REVIEW_31.csv',pids,cols)

groups=defaultdict(list)
for x in pids:groups[x['instance_id']].append(x)
summary=[]
for task,rr in sorted(groups.items()):
 summary.append({'instance_id':task,'n_provisional_fail_runs':len(rr),
 'sample_offsets':' | '.join(f"s{x['sample']}:o{x['offset']}" for x in rr),
 'dispositions':' | '.join(sorted(set(x['semantic_review_status'] for x in rr))),
 'issue_summary':rr[0]['source_issue_title'],
 'primary_concern':rr[0]['failing_assertion'],
 'pr_url':rr[0]['pr_url'],'review_evidence_csv':'STEP6_FAIL_REVIEW_31.csv'})
writecsv('STEP6_TASK_SUMMARY_15.csv',summary,list(summary[0]))

heading='''# Step 6 — Independent-issue-aligned review of provisional FAIL tests

**Research project:** SWE-ABS Free Evaluation  
**Review date:** November 12, 2026  
**Input:** archived `sweabs_full_198_cumulative_v2.csv` (198 rows: 153 PASS / 31 FAIL / 14 UNVERIFIED)  
**Review scope:** **31 provisional FAIL runs from 15 distinct task IDs**, grouped by issue and by exact failing sample.  
**Method:** AI-assisted documentary comparison of original task requirements and **verified upstream merged GitHub PRs**, the SWE-ABS enhanced test patch, and each run's raw `test_output.txt`. Rechecked per-run patch and test patch hashes and base commit. Two external standards and Python official documentation were consulted when pertinent. **No new execution of original repositories, no independent human/maintainer assessment, no adjudication of PASS or UNVERIFIED, and no label changes.**

## Semantic review statuses (not benchmark labels)

| Status | Interpretation | Runs |
| --- | --- | ---: |
'''
labels={
 'valid_failure':'Issue-aligned failure with at least one substantively defensible failing assertion (still provisional)',
 'invalid_test':'Observed failing assertion is demonstrably contradictory to the cited specification or irrelevant to original issue',
 'environment_sensitive':'Test failure depends on runtime/descriptor/backend behavior and needs controlled comparability check',
 'unresolved':'Issue scope, test expectation, or internal contract insufficiently established by available sources'
}
for k in ('valid_failure','invalid_test','environment_sensitive','unresolved'):
 heading+=f'| `{k}` | {labels[k]} | {cs[k]} |\n'
heading+='''
**All 31 cases receive an explicit disposition, but this is **not** a new 31-case binary PASS/FAIL truth set. The v2 runner outcome remains FAIL in every reviewed row; semantic strength is assessed separately. Reclassifying/deleting an outcome requires a new versioned policy at Step 7.**

### Research-validity rules

1. A raw strengthened-test failure alone is not proof of task-appropriate failure. Check the specific *failing assertion*, not simply the test suite name or gold reference patch.
2. An assertion may be consistent with the gold patch yet impose an additional undocumented behavior. Gold implementation conformity is not the only possible correct fix.
3. If multiple samples fail the identical strengthened test, they are repeated **agent runs on the same task**, not independent confirmations that the test assertion is valid.
4. A `valid_failure` here means **documentary support for the assertion's relevance and expected result**, not independently executed semantic proof. Treat as reviewed provisional until reproducible issue-relevant checks or a human/maintainer oracle backs it.
5. Preserve competing explanations and versioned source evidence. An `invalid_test` or `environment_sensitive` label must not silently turn the original runner outcome into a PASS.

## Per-task judgments and citations

'''
md=heading
for t,rr in sorted(groups.items()):
 x=rr[0]; status=Counter(y['semantic_review_status'] for y in rr)
 md+=f"### {t} — {len(rr)} FAIL run(s)\n\n"
 md+=f"**Upstream reference:** [{x['source_issue_title']}]({x['pr_url']}). **Review decisions:** "+", ".join(f"{k}={v}" for k,v in sorted(status.items()))+".\n\n"
 md+=f"**Failing assertion:** {x['failing_assertion']}\n\n"
 md+=f"**Issue/test assessment:** {x['review_reason']}\n\n"
 md+=f"**Opposing interpretation:** {x['opposing_interpretation']}\n\n"
 if x['independent_standard_docs']:
  md+="**Independent standard/documentation:** "+", ".join(f"[{u}]({u})" for u in x['independent_standard_docs'].split(' | '))+".\n\n"
 for r in rr:
  if r['review_reason']!=x['review_reason']:
   md+=f"**Sample {r['sample']} offset {r['offset']} exception (`{r['semantic_review_status']}`):** {r['review_reason']} **Counterview:** {r['opposing_interpretation']}\n\n"
  md+=f"- Sample {r['sample']} offset {r['offset']}: `{r['semantic_review_status']}`; observed failures: `{r['observed_failed_subtests'][:230]}`; [GitHub raw evidence]({r['raw_run_url']}); test SHA-256 `{r['test_patch_sha256']}`.\n"
 md+=f"\n**Next review action:** {x['next_validation_action']}\n\n"
md+='''## Three high-impact validity flags

### 1. Django RFC850 centuries: demonstrably wrong failing expectation

The enhanced test mocks a current time of July 1, **2099**, then asserts that a two-digit \'00\' year on January 1 must mean **2000**. The actual parser gives **2100**. [RFC7231 §7.1.1.1](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1) requires mapping an rfc850-date to the past century **only when it would otherwise be more than 50 years in the future**. January 2100 is less than a year after July 2099. Thus the specific failing expectation is inconsistent with its own normative rule. This affects three runs of the *same task*, not three independent mistakes in standards interpretation.

### 2. SymPy determinant: unrelated auxiliary helper API

The enhanced failing assertion calls `random_complex_number(rational=True, tolerance=1e-3)`, producing `TypeError: unexpected keyword argument 'tolerance'`. The [upstream PR #13877](https://github.com/sympy/sympy/pull/13877) and task describe Bareiss determinant zero-pivot handling, not a required public `randtest` tolerance option. Although the reference patch included an auxiliary tolerance API, independent determinant-correct implementations may not. Therefore this is a stronger-test *scope* problem, not demonstrated failure of the user-reported determinant behavior.

### 3. Django ModelForm Python 3.9 descriptor compatibility

The enhanced tests introduce class attributes `formfield_callback = staticmethod(class_callback)`. Two tests fail with `TypeError: formfield_callback must be a function or callable` in a **Python 3.9** runner. [Python's documentation](https://docs.python.org/3/library/functions.html#staticmethod) states that `staticmethod` objects became directly callable **in Python 3.10**, so these tests are interpreter-sensitive. The [upstream Django PR #15916](https://github.com/django/django/pull/15916) says both class-level and `Meta` callbacks should be supported. The desired priority when both are present needs separate assessment.

## Remaining work and separation of phases

- **Step 6 documentary review complete:** Every provisional FAIL has a recorded status, raw-run provenance, issue/PR link, assertions, alternative explanation, and concrete next review action. The review is limited by the absence of issue-specific oracle reruns, human/maintainer adjudication, and complete environment cross-testing.
- **Step 7 next:** Triage the 14 UNVERIFIED cases; define a frozen analysis label manifest that clearly distinguishes raw runner verdict, reviewed semantic status, exclusions, and alternative sensitivity scenarios. Do not automatically relabel invalid-test rows as PASS. Document any reruns or stronger oracle as separately versioned evidence.
- **Do not claim predictive associations:** trajectory process indicators and statistical analyses have not yet been computed.

## File and source index

- [Current v2 198-row runner outcomes](sweabs_full_198_cumulative_v2.csv) (unchanged)
- [Step 6 full 31-row review table](STEP6_FAIL_REVIEW_31.csv)
- [Step 6 15-task summary](STEP6_TASK_SUMMARY_15.csv)
- [Earlier 83-run re-audit](STEP5_RECONCILIATION_REPORT.md)
- [Original raw evidence and SHA-256 manifest](MANIFEST.md) (raw archives private; links and checksums there)
- [RFC7231 §7.1.1.1](https://www.rfc-editor.org/rfc/rfc7231.html#section-7.1.1.1); [RFC3986 §3.2.1](https://www.rfc-editor.org/rfc/rfc3986.html#section-3.2.1); [RFC1738 §3.1](https://www.rfc-editor.org/rfc/rfc1738.html#section-3.1); [Python staticmethod history](https://docs.python.org/3/library/functions.html#staticmethod)
'''
(OUT/'STEP6_FAIL_VALIDITY_REVIEW.md').write_text(md,encoding='utf8')
print('written',[(f.name,f.stat().st_size) for f in OUT.iterdir()])
