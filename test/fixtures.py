"""
PyTest Fixtures
테스트 코드를 조직하고 테스트 환경을 설정하는 데 사용되는 도구
테스트 케이스를 작성할 때, 공통적으로 필요한 설정, 데이터, 리소스를 테스트 간에 공유하거나 활용할 수 있도록 하는 것
"""

from hook import *
import pytest


@pytest.fixture
def signup_data(login_data):
    yield {
        "username": "pytestuser",
        "password": "password",
        "email": "pytest@test.com"
    }

    delete_user(login_data)


@pytest.fixture
def signup_another_data(login_another_data):
    yield {
        "username": "anotherpytestuser",
        "password": "password",
        "email": "anotherpytest@test.com"
    }

    delete_user(login_another_data)


@pytest.fixture
def login_data():
    yield {
        "username": "pytestuser",
        "password": "password"
    }


@pytest.fixture
def login_another_data():
    yield {
        "username": "anotherpytestuser",
        "password": "password"
    }


@pytest.fixture
def post_data():
    yield {
        "post": {
            "title": "PyTest Title",
            "content": "Pytest Content"
        },
        "ingredients": []
    }


@pytest.fixture
def comment_data():
    yield {
        "content": "PyTest Comment"
    }
