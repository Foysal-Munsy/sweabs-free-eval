#!/usr/bin/env python3
"""Versioned follow-up full-module check, distinct from targeted 1-method probes.

This wrapper uses EXACT SAME source pinning and model/test patch integrity as
step11_django_backend_probe.py but selects the full augmented test file/module.
Historical v2 and Step 7 labels remain immutable.
"""
from __future__ import annotations
import argparse
import step11_django_backend_probe as probe

APPROVED={
    "django__django-15503":("model_fields.test_jsonfield_numeric_keys",["supports_json_field_contains"]),
    "django__django-14434":("schema.tests",["supports_expression_indexes","supports_covering_indexes"]),
}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("phase",choices=["prepare","execute"])
    ap.add_argument("--task",choices=tuple(APPROVED),required=True)
    ap.add_argument("--sample",type=int,choices=(1,2,3),required=True)
    args=ap.parse_args()
    module,features=APPROVED[args.task]
    probe.ALLOWED[args.task]={"method":module,"feature_flags":features}
    if args.phase=="prepare":probe.prepare(args.task,args.sample)
    else:probe.execute(args.task,args.sample)
if __name__=="__main__":main()
