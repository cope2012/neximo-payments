import jwt
from django.test import TestCase
from http import HTTPStatus
from django.contrib.auth import get_user_model
from users.custom_auth import CustomAuth
from django.test.client import RequestFactory
from rest_framework import exceptions
from unittest import mock
import datetime

DEFAULT_PASSWORD = "superpassword"


def create_user(
    client,
    name="John Doe",
    email="john@gmail.com",
    password=DEFAULT_PASSWORD,
):
    response = client.post(
        "/api/register",
        data={
            "name": name,
            "email": email,
            "password": password
        }
    )
    return response


def login_user(client, email="john@gmail.com", password=DEFAULT_PASSWORD):
    login_resp = client.post(
        "/api/login",
        data={
            "email": email,
            "password": password
        }
    )

    return login_resp


class TestUsersViews(TestCase):
    def test_register_user(self):
        response = create_user(self.client)
        data = response.json()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        assert "name" in data
        assert "email" in data
        users_count = get_user_model().objects.all().count()
        self.assertEqual(users_count, 1)

    def test_cant_create_user_due_to_invalid_payload(self):
        response = create_user(self.client, password="")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_login_user(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        self.assertEqual(login_resp.status_code, HTTPStatus.OK)
        data = login_resp.json()
        assert "access" in data

    def test_cant_login_due_to_user_not_found(self):
        create_user(self.client)
        login_resp = login_user(self.client, email="jane@gmail.com")
        self.assertEqual(login_resp.status_code, HTTPStatus.UNAUTHORIZED)

    def test_change_password(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        change_password_resp = self.client.post(
            "/api/password",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data={
                "old_password": DEFAULT_PASSWORD,
                "new_password": "anothergoodpassword"
            }
        )
        self.assertEqual(change_password_resp.status_code, HTTPStatus.OK)

        login_resp = self.client.post(
            "/api/login",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data={
                "email": "john@gmail.com",
                "password": "anothergoodpassword"
            }
        )
        self.assertEqual(login_resp.status_code, HTTPStatus.OK)

    def test_cant_change_password_due_to_missmatch(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        change_password_resp = self.client.post(
            "/api/password",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data={
                "old_password": "thispasswordiswrong",
                "new_password": "anothergoodpassword"
            }
        )
        self.assertEqual(change_password_resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_cant_change_password_due_to_password_are_equals(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        change_password_resp = self.client.post(
            "/api/password",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data={
                "old_password": "anothergoodpassword",
                "new_password": "anothergoodpassword"
            }
        )
        self.assertEqual(change_password_resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_cant_change_password_due_to_invalid_payload(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        change_password_resp = self.client.post(
            "/api/password",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}"
            },
            data={
                "old_password": DEFAULT_PASSWORD,
                "new_password": ""
            }
        )
        self.assertEqual(change_password_resp.status_code, HTTPStatus.BAD_REQUEST)

    def test_cant_change_password_due_to_invalid_token(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        change_password_resp = self.client.post(
            "/api/password",
            headers={
                "Authorization": f"Bearer {login_resp.json()['access']}notvalid"
            },
            data={
                "old_password": DEFAULT_PASSWORD,
                "new_password": "anothergoodpassword"
            }
        )
        self.assertEqual(change_password_resp.status_code, HTTPStatus.FORBIDDEN)


class TestCustomAuth(TestCase):
    def test_no_auth_headers(self):
        custom_auth = CustomAuth()
        request = RequestFactory().post('/api/payments')
        resp = custom_auth.authenticate(request)
        assert resp is None

    def test_invalid_token(self):
        custom_auth = CustomAuth()
        request = RequestFactory().post('/api/payments')
        request.headers = {
            "Authorization": f"Bearer kj"
        }
        try:
            custom_auth.authenticate(request)
            assert False
        except exceptions.AuthenticationFailed as e:
            assert str(e) == 'token not valid'

    @mock.patch('jwt.decode')
    def test_token_expired(self, validate_mock):
        create_user(self.client)
        login_resp = login_user(self.client)
        custom_auth = CustomAuth()
        request = RequestFactory().post('/api/payments')
        request.headers = {
            "Authorization": f"Bearer {login_resp.json()['access']}"
        }
        validate_mock.side_effect = jwt.ExpiredSignatureError()
        try:
            custom_auth.authenticate(request)
            assert False
        except exceptions.AuthenticationFailed as e:
            assert str(e) == 'token is expired'

    def test_token_missing_auth_prefix(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        custom_auth = CustomAuth()
        request = RequestFactory().post('/api/payments')
        request.headers = {
            "Authorization": login_resp.json()['access']
        }
        try:
            custom_auth.authenticate(request)
            assert False
        except exceptions.AuthenticationFailed as e:
            assert str(e) == 'missing auth prefix'

    def test_authentication_succeeded(self):
        create_user(self.client)
        login_resp = login_user(self.client)
        custom_auth = CustomAuth()
        request = RequestFactory().post('/api/payments')
        request.headers = {
            "Authorization": f"Bearer {login_resp.json()['access']}"
        }
        user, _ = custom_auth.authenticate(request)
        assert user == get_user_model().objects.first()
