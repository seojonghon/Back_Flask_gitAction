from fixtures import signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data
from hook import *


"""
Unit Tests: Members
회원 관련 API 단위 테스트
"""


# 회원가입 테스트
def test_signup(signup_data, login_data):
    resp = create_user(signup_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 로그인 테스트
def test_login(signup_data, login_data):
    create_user(signup_data)
    resp = login(login_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 로그아웃 테스트
def test_logout(signup_data, login_data):
    create_user(signup_data)
    resp = logout(login_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 사용자 삭제 테스트
def test_delete_user(signup_data, login_data):
    signup_resp = create_user(signup_data)
    resp = delete_user(login_data)
    create_user(signup_data)

    assert resp.status_code == 200
    assert signup_resp.json()['user_id'] == resp.json()['user_id']


# 토큰 리프레시 테스트
def test_refresh(signup_data, login_data):
    create_user(signup_data)
    resp = refresh(login_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


"""
Unit Tests: Posts
레시피 관련 API 단위 테스트
"""


# Unauthenticated 사용자 레시피 등록 실패 테스트
def test_create_post_unauthenticated(post_data):
    resp = create_post_unauthenticated(post_data)

    assert resp.status_code == 401


# Authenticated 사용자 레시피 등록 테스트
def test_create_post_authenticated(signup_data, login_data, post_data):
    resp = create_post_authenticated(signup_data, login_data, post_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 레시피 조회 테스트
def test_get_post(signup_data, login_data, post_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    post = get_post(post_id)

    assert post.json()['post']['title'] == post_data['post']['title']
    assert post.json()['post']['content'] == post_data['post']['content']


# Unauthenticated 사용자 레시피 삭제 테스트
def test_delete_post_unauthenticated(signup_data, login_data, post_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    resp = delete_post(post_id, {})

    assert resp.status_code == 401


# Authenticated 사용자 레시피 삭제 테스트
def test_delete_post_authenticated(signup_data, login_data, post_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    resp = delete_post(post_id, get_tokens(login_data))

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 레시피 업데이트 테스트
def test_update_post(signup_data, login_data, post_data):
    og_post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = og_post_resp.json()['post_id']

    new_post_data = {
        "post": {
            "title": "Pytest Updated Title",
            "content": "Pytest Updated Content"
        },
        "ingredients": []
    }

    resp = update_post(post_id, new_post_data)

    new_post = get_post(post_id)

    assert resp.status_code == 200
    assert new_post.json()['post']['title'] == new_post_data['post']['title']
    assert new_post.json()['post']['content'] == new_post_data['post']['content']


# 자신의 레시피 좋아요 실패 테스트
def test_like_own_post_failure(signup_data, login_data, post_data):
    resp = like_own_post(signup_data, login_data, post_data)

    assert resp.status_code == 400
    assert resp.json()['result'] == 'failed'
    assert resp.json()['message'] == '자신이 작성한 레시피 좋아요 불가'


# 중복 레시피 좋아요 실패 테스트
def test_like_post_duplicated_failure(signup_data, signup_another_data, login_data, login_another_data, post_data):
    _, endpoint, headers = (like_post(
        signup_data, signup_another_data, login_data, login_another_data, post_data))
    resp = requests.post(url=endpoint, headers=headers)

    assert resp.status_code == 400
    assert resp.json()['result'] == 'failed'
    assert resp.json()['message'] == '중복 좋아요 불가'


# 레시피 좋아요 테스트
def test_like_post(signup_data, signup_another_data, login_data, login_another_data, post_data):
    resp, _, _ = (like_post(
        signup_data, signup_another_data, login_data, login_another_data, post_data))

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 댓글 작성 테스트
def test_create_comment(signup_data, login_data, post_data, comment_data):
    _, resp = create_comment(signup_data, login_data, post_data, comment_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 자신의 댓글 좋아요 실패 테스트
def test_like_own_comment_failure(signup_data, login_data, post_data, comment_data):
    resp = like_own_comment(signup_data, login_data, post_data, comment_data)

    assert resp.status_code == 400
    assert resp.json()['result'] == 'failed'
    assert resp.json()['message'] == '자신이 작성한 댓글 좋아요 불가'


# 중복 좋아요 실패 테스트
def test_like_comment_duplicated_failure(
        signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data):
    _, endpoint, headers = like_comment(
        signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data)
    resp = requests.post(url=endpoint, headers=headers)

    assert resp.status_code == 400
    assert resp.json()['result'] == 'failed'
    assert resp.json()['message'] == '중복 좋아요 불가'


# 댓글 좋아요 테스트
def test_like_comment(
        signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data):
    resp, _, _ = like_comment(signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 댓글 수정 테스트
def test_modify_comment(signup_data, login_data, post_data, comment_data):
    resp = modify_comment(signup_data, login_data, post_data, comment_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'


# 댓글 삭제 테스트
def test_delete_comment(signup_data, login_data, post_data, comment_data):
    resp = delete_comment(signup_data, login_data, post_data, comment_data)

    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'
