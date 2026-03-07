import requests

BASE = 'http://localhost:8000'


def test_health():
    r = requests.get(f'{BASE}/health')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'


def test_search_found():
    r = requests.get(f'{BASE}/api/v1/search', params={'village': 'Kisanpur', 'survey': '123'})
    assert r.status_code == 200
    data = r.json()
    assert data['count'] >= 1
    assert any(p['village'] == 'Kisanpur' for p in data['results'])


def test_case_detail():
    r = requests.get(f'{BASE}/api/v1/search', params={'village': 'Kisanpur', 'survey': '123'})
    data = r.json()
    assert data['count'] >= 1
    case_id = data['results'][0]['linked_cases'][0]['case_id']
    from urllib.parse import quote
    r2 = requests.get(f"{BASE}/api/v1/cases/{quote(case_id, safe='')}" )
    assert r2.status_code == 200
    c = r2.json()
    assert c['case_id'] == case_id
