"""Standard-library unit tests for frozen Step 8 indicator implementation.
Synthetic traces only: no label, no live dataset, no regression leakage.
Run: python -m unittest discover -s tests -p 'test_step9_indicators.py' -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from step9_extract_trajectory_features import extract,VERIFY

def call(name,ident,args=None):
    return {"id":ident,"function":{"name":name,"arguments":args or {}}}

def assistant(*calls):
    return {"role":"assistant","tool_calls":list(calls)}

def obs(ident,code=0):
    return {"role":"tool","tool_call_id":ident,
            "content":"{'exit_code': %d, 'is_error': False}" % code}

class FrozenIndicatorsTest(unittest.TestCase):
    def test_django_is_verification(self):
        self.assertIsNotNone(VERIFY.search("./tests/runtests.py modeltests"))
        self.assertIsNone(VERIFY.search("echo unknown_script.py"))

    def test_repeat_error_editor_order(self):
        messages=[
            assistant(call("terminal","a",{"command":"pytest   -q"})),obs("a",0),
            assistant(call("terminal","b",{"command":"pytest -q"})),obs("b",1),
            assistant(call("file_editor","e",{"path":"x"})),
            assistant(call("terminal","c",{"command":"./tests/runtests.py app"})),obs("c",0),
            assistant(call("file_editor","f",{"path":"y"})),
        ]
        f=extract({"messages":messages,"n_steps":5})
        expected={
            "tool_calls_total":5,"terminal_calls":3,"editor_calls":2,"verification_commands":3,
            "duplicate_terminal_commands":1,"immediate_duplicate_terminal_commands":1,
            "terminal_errors_observed":1,"editor_after_last_verification":1,"any_verification":1,
            "duplicate_terminal_rate":"0.333333333333","terminal_error_rate":"0.333333333333",
            "error_coverage_complete":1}
        for k,v in expected.items():self.assertEqual(f[k],v,k)

    def test_missing_terminal_reply_stays_missing(self):
        f=extract({"messages":[assistant(call("terminal","x",{"command":"ls"}))]})
        self.assertEqual(f["terminal_errors_observed"],"")
        self.assertEqual(f["terminal_error_rate"],"")
        self.assertEqual(f["error_coverage_complete"],0)
        self.assertEqual(f["any_verification"],0)
        self.assertEqual(f["editor_after_last_verification"],"")

    def test_only_editor_no_verification(self):
        f=extract({"messages":[assistant(call("file_editor","e",{"path":"a"}))]})
        self.assertEqual(f["terminal_calls"],0)
        self.assertEqual(f["duplicate_terminal_rate"],"0")
        self.assertEqual(f["terminal_error_rate"],"")
        self.assertEqual(f["editor_after_last_verification"],"")

    def test_malformed_terminal_args_rejected(self):
        with self.assertRaises(ValueError):
            extract({"messages":[assistant(call("terminal","e",{"not_command":"x"}))]})

if __name__=="__main__":unittest.main()
