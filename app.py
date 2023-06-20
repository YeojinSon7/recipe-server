from flask import Flask
from flask_restful import Api
from config import Config
from resources.recipe import MyRecipeListResource, RecipeListResource, RecipePublishResource, RecipeResource
from resources.user import UserLoginResource, UserLogoutResource, UserRecipeResource, UserRegisterResource, jwt_blocklist

from flask_jwt_extended import JWTManager


app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)

# 로그아웃된 토큰으로 요청하는 경우! 이 경우는 비정상적인 경우
# jwt가 알아서 처리하도록 코드작성
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)

# 경로와 API동작코드(Resource)를 연결한다
api.add_resource(  RecipeListResource ,'/recipes')
api.add_resource(  RecipeResource ,  '/recipes/<int:recipe_id>') # 클라이언트에게 url에 숫자들어오면 그건 recipe_id야 니가 처리해
api.add_resource(  UserRegisterResource ,'/user/register')
api.add_resource(  UserLoginResource ,'/user/login')
api.add_resource(   UserLogoutResource ,'/user/logout')
api.add_resource(  UserRecipeResource ,'/user/<int:user_id>')
api.add_resource(  RecipePublishResource  , '/recipes/<int:recipe_id>/publish' )
api.add_resource(   MyRecipeListResource  ,'/recipes/me')

if __name__ == '__main__' :
    app.run()

