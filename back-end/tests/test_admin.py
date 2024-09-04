import pytest
import os

def test_admin_register(admin_register):
    pass

def test_admin_login(admin_token):
    admin_token()

def test_health_check(admin_client):
    response = admin_client().get("healthcheck/")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload.keys() == {"status", "dataconnection"}, payload
    assert payload["status"] == "OK", payload
    assert payload["dataconnection"], payload
    
def test_resetall(resetall):
    pass

def test_upload_data(upload_data):
    pass

