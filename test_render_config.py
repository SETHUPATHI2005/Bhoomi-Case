import urllib.request
import json
import sys

URL = "https://bhoomi-case.onrender.com/api/v1/auth/email-config-status" # Guessing URL name based on repo
try:
    req = urllib.request.Request(URL)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(f"Diagnostics from {URL}:")
        for k, v in result.items():
            print(f"  {k}: {v}")
except Exception as e:
    print(f"Failed to reach {URL}: {e}")
