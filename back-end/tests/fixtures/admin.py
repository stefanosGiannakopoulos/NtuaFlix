import pytest
import models

@pytest.fixture(scope="session")
def admin_register(client, db_sessionmaker):
    payload = {
            "username":         "test_admin",
            "first_name":       "Test Name",
            "last_name":        "Test Last Name",
            "email":            "test@email.org",
            "dob":              "2002-04-23",
            "password":         "123456",
            "password_confirm": "123456",
            }
    response = client().post("register/", json=payload)
    assert response.status_code == 200, response.text
    
    with db_sessionmaker() as test_db:
        admin = test_db.query(models.User).filter_by(username = "test_admin").first()
        assert admin is not None, "user not added to database"
        admin.is_admin = True
        test_db.commit()


@pytest.fixture(scope="session")
def admin_token(client, admin_register, db_sessionmaker):
    def factory():
        with db_sessionmaker() as test_db:
            admin = test_db.query(models.User).filter_by(username = "test_admin").first()
            assert admin is not None
        data = {
                "username": "test_admin",
                "password": "123456",
                }
        response = client().post("login/", data=data)
        assert response.status_code == 200, response.text

        token = response.json()['token']
        assert token is not None

        return token
    return factory

@pytest.fixture(scope="session")
def admin_client(client, admin_token):
    def factory():
        return client(relative_url="admin/", headers={'X-OBSERVATORY-AUTH': admin_token()})
    return factory

