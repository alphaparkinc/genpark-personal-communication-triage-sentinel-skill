from client import PersonalCommunicationTriageSentinel
import json

sentinel = PersonalCommunicationTriageSentinel()
print("=== PERSONAL COMMUNICATION TRIAGE BENCHMARK ===")
res = sentinel.run_communication_benchmark()
print(json.dumps(res, indent=2))
