"""
테스트 Hook 함수
"""


import requests


BASE_URL = "http://127.0.0.1:5000"


def get_tokens(login_data):
    login_resp = login(login_data)

    if login_resp.status_code == 400:
        raise Exception('Failed to login')

    cookies = login_resp.cookies

    access_token = cookies.get('access_token_cookie')
    csrf_access_token = cookies.get('csrf_access_token')
    refresh_token = cookies.get('refresh_token_cookie')
    csrf_refresh_token = cookies.get('csrf_refresh_token')

    if not access_token or not csrf_access_token or not refresh_token or not csrf_refresh_token:
        raise Exception('One or more tokens are missing in Set-Cookie header')

    return {
        'access_token': access_token,
        'csrf_access_token': csrf_access_token,
        'refresh_token': refresh_token,
        'csrf_refresh_token': csrf_refresh_token
    }


def set_headers(tokens):
    return {
        'Cookie': f'access_token_cookie={tokens["access_token"]};'
                  f'refresh_token_cookie={tokens["refresh_token"]}',
        "X-CSRF-Token": tokens["csrf_access_token"],
        'X-CSRF-Refresh-Token': tokens["csrf_refresh_token"]
    }


def create_user(signup_data):
    endpoint = f'{BASE_URL}/members/forms'

    return requests.post(url=endpoint, json=signup_data)


def delete_user(login_data):
    login_resp = login(login_data)
    tokens = get_tokens(login_data)
    user_id = login_resp.json()['user_id']

    endpoint = f'{BASE_URL}/members/{user_id}'

    return requests.delete(url=endpoint, headers=set_headers(tokens))


def login(login_data):
    endpoint = BASE_URL + '/members/login'

    return requests.post(url=endpoint, json=login_data)


def logout(login_data):
    endpoint = BASE_URL + '/members/logout'
    tokens = get_tokens(login_data)

    return requests.post(url=endpoint, headers=set_headers(tokens))


def refresh(login_data):
    endpoint = BASE_URL + '/members/tokens'
    tokens = get_tokens(login_data)

    return requests.get(url=endpoint, headers=set_headers(tokens))


def create_post_authenticated(signup_data, login_data, post_data):
    create_user(signup_data)
    tokens = get_tokens(login_data)

    endpoint = BASE_URL + '/posts/forms'

    return requests.post(url=endpoint, json=post_data, headers=set_headers(tokens))


def create_post_unauthenticated(post_data):
    endpoint = BASE_URL + '/posts/forms'

    return requests.post(url=endpoint, json=post_data)


def get_post(post_id):
    endpoint = f'{BASE_URL}/posts/{post_id}'

    return requests.get(url=endpoint)


def update_post(post_id, new_post_data):
    endpoint = f'{BASE_URL}/posts/forms/{post_id}'

    return requests.put(url=endpoint, json=new_post_data)


def delete_post(post_id, tokens):
    endpoint = f'{BASE_URL}/posts/{post_id}'

    if not tokens:
        return requests.delete(url=endpoint)
    else:
        return requests.delete(url=endpoint, headers=set_headers(tokens))


def like_own_post(signup_data, login_data, post_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    endpoint = BASE_URL + f'/posts/{post_id}/likes'
    tokens = get_tokens(login_data)

    return requests.post(url=endpoint, headers=set_headers(tokens))


def like_post(signup_data, signup_another_data, login_data, login_another_data, post_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    endpoint = BASE_URL + f'/posts/{post_id}/likes'
    create_user(signup_another_data)
    tokens = get_tokens(login_another_data)
    headers = set_headers(tokens)

    return requests.post(url=endpoint, headers=headers), endpoint, headers


def create_comment(signup_data, login_data, post_data, comment_data):
    post_resp = create_post_authenticated(signup_data, login_data, post_data)
    post_id = post_resp.json()['post_id']

    endpoint = f'{BASE_URL}/posts/{post_id}/comments'
    tokens = get_tokens(login_data)

    return post_id, requests.post(url=endpoint, json=comment_data, headers=set_headers(tokens))


def like_own_comment(signup_data, login_data, post_data, comment_data):
    post_id, comment_resp = create_comment(signup_data, login_data, post_data, comment_data)
    comment_id = comment_resp.json()['comment_id']

    endpoint = f'{BASE_URL}/posts/comments/{comment_id}/likes'
    tokens = get_tokens(login_data)

    return requests.post(url=endpoint, headers=set_headers(tokens))


def like_comment(signup_data, login_data, signup_another_data, login_another_data, post_data, comment_data):
    post_id, comment_resp = create_comment(signup_data, login_data, post_data, comment_data)
    comment_id = comment_resp.json()['comment_id']

    create_user(signup_another_data)

    endpoint = f'{BASE_URL}/posts/comments/{comment_id}/likes'
    tokens = get_tokens(login_another_data)
    headers = set_headers(tokens)

    return requests.post(url=endpoint, headers=headers), endpoint, headers


def modify_comment(signup_data, login_data, post_data, comment_data):
    _, comment_resp = create_comment(signup_data, login_data, post_data, comment_data)
    comment_id = comment_resp.json()['comment_id']

    endpoint = f'{BASE_URL}/posts/comments/{comment_id}'
    new_comment_data = {
        "content": "PyTest Updated Comment"
    }
    tokens = get_tokens(login_data)

    return requests.put(url=endpoint, json=new_comment_data, headers=set_headers(tokens))


def delete_comment(signup_data, login_data, post_data, comment_data):
    _, comment_resp = create_comment(signup_data, login_data, post_data, comment_data)
    comment_id = comment_resp.json()['comment_id']

    endpoint = f'{BASE_URL}/posts/comments/{comment_id}'
    tokens = get_tokens(login_data)

    return requests.delete(url=endpoint, headers=set_headers(tokens))
