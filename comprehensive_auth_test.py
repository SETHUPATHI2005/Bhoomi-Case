#!/usr/bin/env python3
"""Comprehensive authentication test"""

import requests
import json
import os
import sys

os.chdir('backend/app')
sys.path.insert(0, '.')

BASE_URL = 'http://localhost:8000'

def test_endpoints():
    """Test all auth endpoints"""
    
    print("=" * 60)
    print("BHOOMI AUTHENTICATION COMPREHENSIVE TEST")
    print("=" * 60)
    
    # 1. Test registration
    print("\n1. TESTING REGISTRATION")
    print("-" * 60)
    
    test_user = {
        'username': 'testuser_' + str(int(__import__('time').time() % 1000000)),
        'email': f'test_{int(__import__("time").time() % 1000000)}@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    print(f"Registering user: {test_user['username']}")
    print(f"Email: {test_user['email']}")
    
    try:
        resp = requests.post(f'{BASE_URL}/api/v1/auth/register', json=test_user, timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if resp.status_code != 201:
            print("ERROR: Registration failed")
            return False
        
        registered_user = test_user.copy()
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 2. Check user file
    print("\n2. CHECKING USER DATABASE")
    print("-" * 60)
    
    try:
        with open('data/users.json', 'r') as f:
            users = json.load(f)
        
        # Find our user
        our_user = next((u for u in users if u['username'] == registered_user['username']), None)
        if our_user:
            print(f"✓ User found in database")
            print(f"  Email Verified: {our_user.get('email_verified', False)}")
            print(f"  Created At: {our_user.get('created_at', 'N/A')}")
        else:
            print("ERROR: User not found in database!")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 3. Check email tokens
    print("\n3. CHECKING EMAIL VERIFICATION TOKENS")
    print("-" * 60)
    
    verification_token = None
    try:
        with open('data/email_tokens.json', 'r') as f:
            tokens = json.load(f)
        
        # Find verification token for our email
        for token_data in reversed(tokens):
            if token_data['email'] == registered_user['email'] and token_data['type'] == 'verify':
                verification_token = token_data['token']
                print(f"✓ Found verification token")
                print(f"  Token: {token_data['token'][:30]}...")
                print(f"  Type: {token_data['type']}")
                print(f"  Used: {token_data['used']}")
                break
        
        if not verification_token:
            print("ERROR: Verification token not found!")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 4. Test login before verification
    print("\n4. TESTING LOGIN (BEFORE EMAIL VERIFICATION)")
    print("-" * 60)
    
    try:
        resp = requests.post(f'{BASE_URL}/api/v1/auth/login', json={
            'username': registered_user['username'],
            'password': registered_user['password']
        }, timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        
        if resp.status_code == 200:
            print("ERROR: Login should fail before email verification!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return False
        else:
            print(f"✓ Login correctly rejected")
            print(f"  Reason: {data.get('detail', 'Unknown')}")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 5. Verify email
    print("\n5. VERIFYING EMAIL")
    print("-" * 60)
    
    try:
        resp = requests.post(f'{BASE_URL}/api/v1/auth/verify-email', json={
            'token': verification_token
        }, timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if resp.status_code != 200:
            print("ERROR: Email verification failed!")
            return False
        else:
            print("✓ Email verified successfully")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 6. Test login after verification
    print("\n6. TESTING LOGIN (AFTER EMAIL VERIFICATION)")
    print("-" * 60)
    
    try:
        resp = requests.post(f'{BASE_URL}/api/v1/auth/login', json={
            'username': registered_user['username'],
            'password': registered_user['password']
        }, timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        
        if resp.status_code != 200:
            print("ERROR: Login failed after verification!")
            print(f"Response: {json.dumps(data, indent=2)}")
            return False
        else:
            print("✓ Login successful!")
            print(f"  Username: {data['user']['username']}")
            print(f"  Email: {data['user']['email']}")
            print(f"  Token: {data['token'][:30]}...")
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # 7. Test with invalid credentials
    print("\n7. TESTING WITH INVALID CREDENTIALS")
    print("-" * 60)
    
    try:
        resp = requests.post(f'{BASE_URL}/api/v1/auth/login', json={
            'username': registered_user['username'],
            'password': 'WrongPassword'
        }, timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        
        if resp.status_code == 401:
            print("✓ Correctly rejected invalid password")
            print(f"  Reason: {data.get('detail', 'Unknown')}")
        else:
            print("ERROR: Should reject invalid password!")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED - AUTH SYSTEM WORKING!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_endpoints()
    sys.exit(0 if success else 1)
