import json
import requests
import os

# Change to app directory
os.chdir('backend/app')

# Check users in the file
print("=== Checking Users File ===")
users = json.load(open('data/users.json'))
print(f"Total users: {len(users)}")
if users:
    user = users[-1]
    print(f"Last user: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Email Verified: {user.get('email_verified', False)}")

# Check email tokens
print("\n=== Checking Email Tokens ===")
try:
    tokens = json.load(open('data/email_tokens.json'))
    print(f"Total email tokens: {len(tokens)}")
    if tokens:
        token = tokens[-1]
        print(f"Latest token - Email: {token['email']}, Type: {token['type']}, Used: {token['used']}")
except:
    print("No email tokens file yet")

# Test login without verification
print("\n=== Testing Login (should fail - not verified) ===")
try:
    response = requests.post('http://localhost:8000/api/v1/auth/login', json={
        'username': 'testuser999',
        'password': 'TestPass123'
    }, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Get the verification token
print("\n=== Getting Verification Token ===")
tokens = json.load(open('data/email_tokens.json'))
verify_token = None
for token_data in reversed(tokens):
    if token_data['email'] == 'testuser999@example.com' and token_data['type'] == 'verify':
        verify_token = token_data['token']
        break

if verify_token:
    print(f"Found verification token: {verify_token[:20]}...")
    
    # Verify email
    print("\n=== Verifying Email ===")
    try:
        response = requests.post('http://localhost:8000/api/v1/auth/verify-email', json={
            'token': verify_token
        }, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Try login again
    print("\n=== Testing Login (after verification) ===")
    try:
        response = requests.post('http://localhost:8000/api/v1/auth/login', json={
            'username': 'testuser999',
            'password': 'TestPass123'
        }, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Could not find verification token")
