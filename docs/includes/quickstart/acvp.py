from pqblocks_acvp.runner import build_golden_session
from pqblocks_acvp.harness import ConformanceHarness
from pqblocks_acvp.adapters.reference import ReferencePQCAdapter

session = build_golden_session()
harness = ConformanceHarness([ReferencePQCAdapter()])
reports = harness.run_session(session)
rep = reports["Reference-FIPS-Oracle"]
print(f"Executed {rep.total_attempted} cases: {rep.passed} passed (denominator verified: {rep.denominator_verified})")
