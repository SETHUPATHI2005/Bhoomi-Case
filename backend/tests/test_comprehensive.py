import requests
import json
import pytest

BASE = 'http://localhost:8000'
ADMIN_TOKEN = "devtoken123"


class TestHealth:
    def test_health_check(self):
        r = requests.get(f'{BASE}/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'


class TestSearch:
    def test_search_no_results(self):
        r = requests.get(f'{BASE}/api/v1/search', params={'village': 'NonExistent', 'survey': '999'})
        assert r.status_code == 200
        assert r.json()['count'] == 0

    def test_search_with_results(self):
        # This assumes sample data was ingested
        r = requests.get(f'{BASE}/api/v1/search', params={'village': 'Kisanpur', 'survey': '123'})
        assert r.status_code == 200
        data = r.json()
        assert 'count' in data
        assert 'results' in data

    def test_search_missing_params(self):
        r = requests.get(f'{BASE}/api/v1/search', params={'village': 'Test'})
        assert r.status_code == 422  # Validation error


class TestAdmin:
    def test_upload_without_auth(self):
        r = requests.post(f'{BASE}/api/v1/admin/upload', json={"village": "Test", "survey_number": "1"})
        assert r.status_code == 401

    def test_upload_with_invalid_token(self):
        r = requests.post(
            f'{BASE}/api/v1/admin/upload',
            json={"village": "Test", "survey_number": "1"},
            headers={"Authorization": "Bearer invalid"}
        )
        assert r.status_code == 403

    def test_upload_valid_parcel(self):
        payload = {
            "village": "TestVillage",
            "survey_number": "999",
            "linked_cases": ["C999/2024"]
        }
        r = requests.post(
            f'{BASE}/api/v1/admin/upload',
            json=payload,
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'

    def test_audit_logs_without_auth(self):
        r = requests.get(f'{BASE}/api/v1/admin/audit-logs')
        assert r.status_code == 401

    def test_audit_logs_with_auth(self):
        r = requests.get(
            f'{BASE}/api/v1/admin/audit-logs',
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestIngest:
    def test_bulk_ingest(self):
        payload = {
            "parcels": [
                {"village": "IngestTest1", "survey_number": "1001"}
            ],
            "cases": [
                {"case_id": "CT1/2024", "court": "Test Court", "status": "ongoing"}
            ]
        }
        r = requests.post(
            f'{BASE}/api/v1/admin/ingest',
            json=payload,
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
        )
        assert r.status_code == 200
        data = r.json()
        assert data['parcels_ingested'] >= 1
        assert data['cases_ingested'] >= 1


class TestErrorHandling:
    def test_invalid_json_upload(self):
        r = requests.post(
            f'{BASE}/api/v1/admin/upload',
            data="invalid",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}", "Content-Type": "application/json"}
        )
        assert r.status_code in [400, 422]

    def test_case_not_found(self):
        r = requests.get(f'{BASE}/api/v1/cases/NONEXISTENT')
        assert r.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
