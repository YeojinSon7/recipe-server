from passlib.hash import pbkdf2_sha256

from config import Config # sha~ 방식이 단방향암호화 방식이다,숫자가 높아질수록 암호더 복잡하게 한다?

# 1. 원문 비밀번호를, 단방향 암호화 하는 함수
def hash_password(original_password):
    # original_password는 사용자가 넣은 1234
    password = pbkdf2_sha256.hash(original_password + Config.SALT)# random seed값 해커가알아내면 패턴 찾아서 초기화하고 해킹할 수 있다.서버에서 보낸 비번 앞 뒤에 문자열 붙인다 그리고 그상태로 암호화한다
    return password
    
# 2. 유저가 입력한 비번이 맞는지 체크하는 함수
def check_password(original_password, hashed_password) :
    check = pbkdf2_sha256.verify(original_password + Config.SALT,hashed_password)
    return check # true냐 false냐 알아서 해결
