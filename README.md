# SWE-ABS Free Evaluation

This repository is used to evaluate coding-agent patches with **SWE-ABS strengthened tests** using GitHub Actions.

## Goal

The research question is:

> Among coding-agent runs that already pass standard evaluation, do simple trajectory-level messiness indicators predict failure under stronger tests?

This repository handles the **stronger-test evaluation** part.

## Why GitHub Actions?

SWE-ABS evaluation requires Docker.

Kaggle does not provide the Docker setup needed for this evaluation, so GitHub Actions is used as the free Docker-based runner.

## What was the problem?

During the first smoke test, the intended model patch was not active when the tests ran.

The bundled SWE-ABS harness tried several patch commands one after another. One fallback partially applied the patch, and the next fallback treated the already-applied change as reversed and removed it.

Because of this, the initial test result was not trustworthy.

## Fix

The workflow now:

* restores the repository before each patch retry;
* uses safer patch fallback commands;
* prevents GNU `patch` from automatically reversing an applied patch;
* checks the final patch state before running tests.

## Verified Smoke Test

Test instance:

`astropy__astropy-12907`

The workflow confirmed that the intended change was active before testing:

```diff
- cright[-right.shape[0]:, -right.shape[1]:] = 1
+ cright[-right.shape[0]:, -right.shape[1]:] = right
```

Strengthened test result:

```text
11 passed
```

So the single-instance smoke test is now working correctly.

## Current Status

Completed:

* GitHub Actions evaluation setup
* patch-application bug identified
* patch retry logic fixed
* exact patch verified before testing
* smoke test verified with 11/11 tests passing

Next:

* evaluate all 198 standard-PASS trajectories;
* save reliable SWE-ABS PASS/FAIL labels;
* merge those labels with trajectory-level indicators;
* run the final statistical analysis.

## Workflow

The current smoke-test workflow is:

`.github/workflows/sweabs-smoke.yml`
