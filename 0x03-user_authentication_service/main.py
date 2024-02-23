#!/usr/bin/env python3

"""
integration test module.
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
HOME_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Test user register.
    """
    url = f"{HOME_URL}/users"
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with wrong password.
    """
    url = f"{HOME_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test user login.
    """
    url = f"{HOME_URL}/sessions"
    body = {
        'email': email,
        'password': password,
    }
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test getting profile information whilst logged out.
    """
    url = f"{HOME_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Test getting profile while logged in.
    """
    url = f"{HOME_URL}/profile"
    req_cookies = {
        'session_id': session_id,
    }
    response = requests.get(url, cookies=req_cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    Test logout.
    """
    url = f"{HOME_URL}/sessions"
    req_cookies = {
        'session_id': session_id,
    }
    response = requests.delete(url, cookies=req_cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Test password reset.
    """
    url = f"{HOME_URL}/reset_password"
    body = {'email': email}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test user password update.
    """
    url = f"{HOME_URL}/reset_password"
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    response = requests.put(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
