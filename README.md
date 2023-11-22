# 한끼얼마 Backend Flask Application Report
## 1. 🥙 한끼얼마 💰
### 1.1 개발 인원

- 1인 개발 (배승원)

### 1.2. 기술 스택 및 환경
#### 1.2.1. 기술 스택

![Static Badge](https://img.shields.io/badge/Python3-3776AB?logo=Python&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/Flask-000000?logo=Flask&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/PostgreSQL-4169E1?logo=PostgreSQL&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/SQLite-000000?logo=SQLite&logoColor=%23FFFFFF) 

#### 1.2.2. 개발 환경

![Static Badge](https://img.shields.io/badge/Mac%20OS%20Ventura-%23000000?logo=Apple&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/PyCharm-%23000000?logo=PyCharm&logoColor=%23FFFFFF)

#### 1.2.3. 스테이징 환경

![Static Badge](https://img.shields.io/badge/Groom-3693F3?logo=iCloud&logoColor=FFFFFF)  ![Static Badge](https://img.shields.io/badge/Ubuntu-333333?logo=Linux%20Containers&logoColor=FFFFFF)

#### 1.2.4. 운영 환경

![Static Badge](https://img.shields.io/badge/Docker-2496ED?logo=Docker&logoColor=FFFFFF) ![Static Badge](https://img.shields.io/badge/K8s-326CE5?logo=Kubernetes&logoColor=FFFFFF)

## 2. 📓 디렉터리 구조

```
📁 rest-recipe-book
├──── 📁 app
│      ├──── 📁 api
│      ├──── 📄 __init__.py
│      └──── 📄 models.py
├──── 📁 config
│      ├──── 📄 __init__.py
│      ├──── 📄 default.py
│      ├──── 📄 develoment.py
│      └──── 📄 production.py
├──── 📁 test
├──── 📄 app.db
├──── 📄 requirements.txt
└──── 📄 README.md
```

## 3. 📃 한끼얼마 API 명세서

> [🖋️ 상세 API 명세서 및 요청 & 응답 예시](https://wonsoong.notion.site/BE-Flask-API-04244dd5f68540d096da7b8b3a081575?pvs=4)

## 4. 👀 특징
### 4.1. RESTful API

|Index|Method|URI|Description|
|---|---|---|---|
|1|GET|/posts|레시피 리스트 조회|
|2|GET|/posts/{int:post_id}|레시피 상세 조회|
|3|DELETE|/posts/{int:post_id}|레시피 삭제|
|4|POST|/posts/forms|레시피 신규 등록|
|5|GET|/posts/forms/ingredients|재료 리스트 조회|
|6|GET|/posts/forms/{int:post_id}|레시피 수정 폼|
|7|PUT|/posts/forms/{int:post_id}|레시피 수정 등록|
|8|POST|/posts/{int:post_id}/likes|레시피 좋아요|
|9|POST|/posts/{int:post_id}/comments|댓글 작성|
|10|POST|/posts/comments/likes|댓글 좋아요|
|11|PUT|/posts/comments/{int:comment_id}|댓글 수정|
|12|DELETE|/posts/comments/{int:comment_id}|댓글 삭제|
|13|POST|/members/forms|신규 회원 가입|
|14|POST|/members/login|로그인|
|15|POST|/members/logout|로그아웃|
|16|GET|/members/tokens|JWT 토큰 재발급|

- REST 원칙에 따라 URI 설계

#### 4.1.1. REST 구성 요소
- URI는 **`리소스`** 의 위치를 식별하는 고유 식별자
- HTTP Method는 해당 자원에 대한 **`행위`**
- JSON 형식으로 자원을 **`표현`**

#### 4.1.2. REST 규칙
- URI를 복수 명사로 구성
- 동사로 표현되는 행위는 HTTP 메서드로 표현
- URI를 소문자로만 구성
- / 로 계층 관계를 표현
- HTTP Status Code를 사용해 응답

### 4.2. JWT Token을 통한 사용자 인증 정보 검증

> 사용 라이브러리: flask_jwt_extended, redis

#### 3.2.1. Response Body를 통한 토큰 전달
- 사용자 로그인 시 4개의 인증 토큰을 발급해 Response Body로 클라이언트에 전달
- 처음 설계 시에는 Set-Cookie를 통해 브라우저의 쿠키 저장소에 저장하고, 인증이 필요한 API 사용 시 이를 꺼내 요청하도록 설계하였음
	- 그러나 크롬 브라우저의 새로운 쿠키 정책의 도입 이후 SameSite 속성 값이 Lax로 되어있어 Cookie가 전달이 되지 않는 이슈 발생
	- SameSite 속성 값을 None으로 설정하면 쿠키 전달이 가능하나, Secure 옵션을 True로 설정해야 하며 이는 HTTPS 적용이 되어있지 않은 현재 API 서버에는 적용 불가능
	- 이 이슈는 Cookie의 근본적인 보안 결함에서 기인하였기에 Cookie 대신 브라우저의 Local Storage에 토큰을 저장하는 방식을 채택
- Kakao 로그인 API에서 JWT를 Response Body에 넣어서 보내는 샘플 코드를 레퍼런스로 하여, 이와 비슷한 형식으로 Client에 토큰 전달
- Response Body를 통한 토큰 전달 예시

```json
{  
    "result": "success",  
    "user_id": "user id",
    "username": "username",  
    "access_token": "access token",
    "csrf_token": "csrf token",  
    "refresh_token": "refresh token",
    "csrf_refresh_token": "csrf refresh token",  
    "message": "로그인 성공"  
}
```

#### 4.2.2. JWT 토큰 검증 로직
1. 클라이언트가 Endpoint로 HTTP 요청
2. Flask가 해당 엔드포인트를 처리할 함수를 호출하기 전에 @jwt_required 데코레이터가 요청을 가로챔
3. @jwt_required 데코레이터는 요청에서 JWT 토큰을 추출
	- 토큰은 HTTP 요청 헤더의 Authorization 헤더에서 Bearer 스키마를 사용해 전달됨
4. 추출된 JWT 토큰이 라이브러리에 의해 검증됨
	- JWT 토큰의 서명이 올바른지 확인
	- 토큰이 만료되지 않았는지 확인
	- Claims가 유효한지 확인
5. 요청이 유효하면 해당 엔드포인트를 처리할 함수를 호출하고, 유효하지 않으면 401 Unauthorized Status Code 반환

#### 4.2.3. Refresh Token과 Redis
- JWT Access Token의 탈취 위험을 감안해 만료 기한을 30분으로 아주 짧게 설정
	- 이는 30분마다 사용자는 재로그인을 해야 한다는 것을 의미
- 사용자의 번거로움을 피할 수 있게 로그인 시 만료 기한이 14일인 Refresh Token, Refresh CSRF Token을 추가로 발급
- Refresh Token을 탈취 당하면 공격자에게 Access Token을 재발급 해줄 수 있다는 문제 발생
	- Redis에 각 사용자에 1:1로 매핑되는 Access Token, Refresh Token 쌍을 저장해 해결
- Token Refresh 요청이 들어오면 서버는 Redis를 뒤져 Key: Value 쌍을 검증하고, 해당 검증이 유효할 시에만 Token 재발급

### 4.3. 단위 테스트 코드 작성을 통한 테스트 자동화

> [⚙️ 단위 테스트 실행 영상](https://youtube.com/shorts/meKtduN8dMo?feature=share)

> Source Code: /test/

- 함수 레벨에서 테스트 서버의 API 동작을 검증하는 단위 테스트 코드 작성
- PyTest 테스트 프레임워크 사용
- 모든 API에 대한 성공, 실패 테스트 진행
- 각 단위 테스트는 완전히 독립적
- 테스트 코드의 요소를 Test, Hook, Fixture로 나눔

#### 4.3.1. Test

```python
def test_signup(signup_data, login_data):
    resp = create_user(signup_data)

    # 검증
    assert resp.status_code == 200
    assert resp.json()['result'] == 'success'
```

- 요청에 대한 응답을 검증하는 코드
- Hook 함수를 호출하고, Status Code, Response Message를 통해 Pass 여부를 검증

#### 4.3.2. Hook

```python
def create_user(signup_data):
    endpoint = f'{BASE_URL}/members/forms'

    # API 호출
    return requests.post(url=endpoint, json=signup_data)
```

- Test에 필요한 요청 정보 설정과 실제 API 호출 로직을 수행하는 코드
- 헤더를 세팅하고, 토큰을 받아오는 등의 자주 사용하는 로직을 Hook으로 만들어 재사용성이 증대

#### 4.3.3. Fixture

```python
@pytest.fixture
def signup_data(login_data):
    yield {
        "username": "pytestuser",
        "password": "password",
        "email": "pytest@test.com"
    }

    # yield 키워드를 사용해 테스트가 끝나면 리소스를 삭제하는 로직 실행
    delete_user(login_data)
```

- 테스트 코드를 조작하고, 테스트 환경을 성정하는 데 사용되는 도구
- Python의 yield 키워드를 사용해 한 개의 단위 테스트가 끝나고 리소스를 삭제
	- 단위 테스트 간 리소스 의존이 전혀 없도록 함

### 4.4. 개발 & 테스트, 운영 환경 분리
#### 4.4.1. Development & Testing 환경

> Testing API Server URL: https://rest-recipe-book-dptb.run.goorm.site

- FE 개발을 협업으로 원활하게 진행하기 위해 Flask 애플리케이션을 Testing API 서버에 배포
- 이를 통해 React FE 애플리케이션의 개발 환경의 API 서버의 Base URL을 각자의 localhost로 하지 않고 실시간 업데이트되는 API를 호출해 개발할 수 있었음
- 개발 및 테스트 환경에서는 SQLite DB를 사용
- Testing 서버는 Groom의 컨테이너 호스팅 서비스를 이용
- Testing Server Start Script

```shell
#!/bin/bash

# 가상환경 활성화
source venvs/rest-recipe-book-groom/bin/activate

# 환경 변수 설정
export FLASK_APP=app
export FLASK_DEBUG=true
export APP_CONFIG_FILE=/workspace/rest-recipe-book/config/development.py
export REDIS_HOST=0.0.0.0

# Redis 서버 백그라운드 실행
nohup redis-server &

# Flask 애플리케이션 실행
flask run -h 0.0.0.0 -p 80

# sudo nohup ./start.sh > ./logs/app.out &
```

#### 4.4.2. Production 환경

```python
# /app/__init__.py
# 생략
def create_app():  
    app = Flask(__name__)  
    app.config.from_envvar('APP_CONFIG_FILE')  
  
    """  
    Application Factory Pattern
    """
    CORS(app)  
    db.init_app(app)  
    bcrypt.init_app(app)  
    jwt.init_app(app)  
  
    """  
    DB
    - Development, Staging 환경: SQlite  
    - Production 환경: PostgresSQL  
    환경에 맞는 DB를 자동으로 플러그
    """
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):  
        migrate.init_app(app, db, render_as_batch=True)  
    else:  
        migrate.init_app(app, db)  
  
    """  
    Blueprints
    """  
    from .api import posts, members  
  
    app.register_blueprint(posts.bp)  
    app.register_blueprint(members.bp)  
  
    return app
```

```python
# /config/production.py
from config.default import *  
from dotenv import load_dotenv  
import os  
  
  
load_dotenv(os.path.join(BASE_DIR, '../docker/.env'))  
  
  
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(  
    user=os.getenv('DB_USER'),  
    pw=os.getenv('DB_PASSWORD'),  
    url=os.getenv('DB_HOST'),  
    port=os.getenv('DB_PORT'),  
    db=os.getenv('DB_NAME'))  
  
  
SECRET_KEY = os.getenv('SECRET_KEY')  
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  
  
  
REDIS_HOST = os.getenv('REDIT_HOST')
```

- Flask 애플리케이션을 Application Factory Pattern을 이용해 생성하므로 실행 시 자동으로 환경을 파악하고 그에 맞는 Config 파일을 꽂아서 환경을 구성
- Docker 또는 K8s 배포를 위한 Production 환경을 분리

### 4.5. Object-Relational Mapping

- 객체와 관계형 데이터베이스 간의 상호 작용을 간단하게 만들어주는 프로그래밍 기술 또는 도구
- 데이터베이스 테이블과 OOP 언어 간의 불일치를 해결하고 데이터베이스와 애플리케이션 코드 간의 상호 작용을 추상화
- Python에서는 SQLAlchemy 사용

#### 4.5.1. Workflow
1. 데이터 모델 정의: 데이터베이스 테이블과 매핑될 데이터 모델(클래스)을 정의
2. ORM 설정: ORM을 설정하여 데이터베이스 연결 정보와 데이터 모델 간의 매핑 규칙을 설정
3. CRUD 작업: 애플리케이션 코드에서 ORM을 사용하여 데이터를 CRUD
4. 쿼리 실행: ORM은 개발자가 작성한 ORM 코드를 기반으로 SQL 쿼리를 생성하고 데이터베이스에 전송하여 실행
5. 결과 처리: 데이터베이스에서 반환된 결과를 객체로 변환하거나 필요한 작업을 수행

#### 4.5.2. 예시: Python Code -> SQL query

```python
# Python code
sub_query = db.session.query(Comment.post_id, Comment.content, User.username).join(User, Comment.user_id == User.id).subquery()
```

```sql
-- SQL query
SELECT *
FROM post_list INNER JOIN "User" ON post_list.user_id = "User".id
LEFT OUTER JOIN sub_query ON sub_query.post_id = post_list.id
WHERE post_list.subject ILIKE 'search_value';
```

#### 4.5.3. Flask ORM Library: SQLAlchemy
- Python을 위한 ORM 및 SQL 툴킷 라이브러리
- 데이터데이스와 상호작용하기 위한 도구 제공
- 구성 요소
	- Core: 데이터베이스와 상호작용하기 위한 기본 도구 제공
	- ORM: 데이터베이스와 Python 클래스 사이의 매핑 제공
	- SQLAlchemy: 데이터베이스 테이블을 파이썬 클래스로 정의
	- Session: 세션을 통해 데이터베이스에 대한 트랜잭션을 관리
	- Engine: 데이터베이스에 대한 모든 SQL 작업이 수행됨
	- Query: SQL 쿼리를 생성하고 실행하는 쿼리 빌더를 제공
- DB 관리 명령어
	- flask db migrate: 모델을 생성하거나 변경할 때 사용
	- flask db upgrade: 모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용

#### 4.5.4. Model
- Models.py 파일에 ORM을 사용해 모델을 정의
	- 데이터베이스 테이블과 상호작용하기 위한 클래스를 정의
- 클래스의 각 속성은 매핑되는 테이블의 Column과 일치
- 데이터 유형과 제약 조건 또한 지정

### 4.6. Flask + WSGI = Web Application Server

- 테스트 환경 또는 운영 환경에서는 웹 서버와 웹 애플리케이션 간의 표준 인터페이스인 WSGI를 붙여 실행
- 구현체인 Gunicorn을 5000번 포트에 바인딩해 서비스
- 운영 환경에서는 Gunicorn을 통해 flask를 서비스하고 보안 상 DEBUG 값을 FALSE로 해놓았기 때문에 로그 파일을 INFO 레벨로 파일에 출력하도록 구성

> 참고: `flask run` 명령은 디버깅이 필요한 개발 환경에서만 사용

## 5. 🔧 Issue & Troubleshooting

> ✅: 해결 이슈 ❓: 미해결 이슈

### 5.1. 사용자 삭제 기능 추가 이후 Null 참조 오류 발생

- 신규 기능으로 User를 삭제하는 기능을 추가
- 삭제하려는 사용자가 댓글을 달았을 경우 댓글의 User 참조값이 Null이 되기 때문에 삭제가 불가능하게 되는 에러 발생

> ✅ 해결: ORM Model에서 cascade 옵션 설정으로 자동으로 댓글이 지워지게 함

### 5.2. Cookie를 사용한 Token 전달이 불가능

- 3.2.1.에 언급했던 문제로 Cookie를 사용해 클라이언트로 Token을 전달할 수 없음
- 크롬 브라우저의 새로운 쿠키 정책과, HTTPS를 적용할 수 없는 문제가 원인

> ✅ 해결: Token을 Response Body에 넣어서 Client로 전달하고, 이를 Header에 받는 방식으로 토큰 검증, 실제로 최근 많은 서비스들이 보안을 위해 이렇게 토큰을 전달하고, Client Side에서 Local Storage에 토큰을 저장한다고 함

### 5.3. Access Token 만료 기한 정하기

- Access Token은 보안 상 만료 기한을 아주 짧게 (한 시간 이내) 가져가야 하는데, 사용자가 지속적으로 재인증을 해야 한다는 문제가 발생

> ✅ 해결: 만료 기한이 14일인 Refresh Token을 추가 발급해 Client에 전달하고, 탈취 위험을 감안해 Redis에 각 사용자에 1:1로 매핑되는 Access Token, Refresh Token 쌍을 저장해 해결, 이와 같은 방법으로 JWT를 운용하는 것이 적절
