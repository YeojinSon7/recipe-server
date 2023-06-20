from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from mysql_connection import get_connection
# API 동작하는 코드를 만들기 위해서는 class(클래스)를 만들어야 한다.

# class 란??? 비슷한 데이터끼리 모아놓은 것 (테이블 생각)
# 클래스는 변수와 함수로 구성된 묶음
# 테이블과 다른점: 함수가 있다는 점!!

# API를 만들기 위해서는,
# flask_restful 라이브러리의 Resource 클래스를 상송해서 만들어야 한다. 파이썬에서 상속은 괄호!

class MyRecipeListResource(Resource):
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''select * 
                    from recipe
                    where user_id = %s;'''
            record = (user_id, )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            result_list = cursor.fetchall() # 결과를 다 리스트로 가져온다
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500
        # 데이터 가공이 필요하면 가공 후 클라이언트에 응답한다
        i = 0
        for row in result_list :
        # row는 딕셔너리 형태
            result_list[i]['createdAt']=row['createdAt'].isoformat() # 문자열로 만드는 것
            result_list[i]['updatedAt']=row['updatedAt'].isoformat()
            i = i + 1
        # 센스있는 코드
        return {'result':'success',
                'count':len(result_list),
                'items':result_list}

class RecipePublishResource(Resource):
    @jwt_required()
    def put(self,recipe_id): # 공개하는 API에 대한 함수
        # 1. 클라이언트로부터 데이터 받아온다.
        user_id = get_jwt_identity()
        # 2. DB 처리한다.
        try:
            connection = get_connection()
            query = '''update recipe
                    set is_publish = 1
                    where id = %s and user_id = %s;'''
            record = (recipe_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500
        return{'result':'success'}
    
    @jwt_required() #이걸 함수바로위에 적어야 header부분을 체크한다
    def delete(self,recipe_id): # 임시저장하는 API대한 함수
         # 1. 클라이언트로부터 데이터 받아온다.
        user_id = get_jwt_identity()
        # 2. DB 처리한다.
        try:
            connection = get_connection()
            query = '''update recipe
                    set is_publish = 0
                    where id = %s and user_id = %s;'''
            record = (recipe_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500
        return{'result':'success'}



class RecipeResource(Resource):
    # GET 메소드에서, 경로로 넘어오는 변수는, get 함수의 파라미터로 사용
    def get(self, recipe_id):
        #1. 클라이언트로부터 데이터를 받아온다.
        # 위의 recipe_id에 유저가 입력한 숫자가 담겨있다.
        #2. 데이터베이스에 레시피 아이디로 쿼리한다.
        print(recipe_id)
        try:
            connection = get_connection()
            query = '''select r.*,u.username
                    from recipe r
                    join user u
                        on r.user_id = u.id
                    where r.id = %s;'''
            record = (recipe_id, ) # 튜플형태(recipe_id)로쓰면 안된다 그건 튜플형태가아니라 숫자이다
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            result_list = cursor.fetchall()
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500
        #3. 결과를 클라이언트에 응답한다.
        i = 0
        for row in result_list :
        # row는 딕셔너리 형태
            result_list[i]['createdAt']=row['createdAt'].isoformat() # 문자열로 만드는 것
            result_list[i]['updatedAt']=row['updatedAt'].isoformat()
            i = i + 1
        if len(result_list) != 1:
             return {'result' : 'success','item': {}}
        else:
            return {'result' : 'success','item': result_list[0]}
        
    @jwt_required()
    def put(self,recipe_id):
        #body에 있는 json 데이터를 받아온다.
        data = request.get_json()
        # 1. 클라이언트로부터 데이터 받아온다
        print(recipe_id)
        user_id = get_jwt_identity()
        #2. 데이터베이스에 update한다.
        try :
            connection = get_connection()
            query = '''update recipe
                    set name = %s, description = %s, num_of_servings = %s, cook_time = %s, directions = %s,is_publish = %s
                    where user_id = %s and id = %s;'''
            record = (data['name'],data['description'],data['num_of_servings'],data['cook_time'],data['directions'],data['is_publish'],user_id,recipe_id)
            cursor= connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result': 'fail','error': str(e)},500
        return {'result': 'success'}
    
    @jwt_required()
    def delete(selt,recipe_id):
        # 1. 클라이언트로부터 데이터 받아온다
        print(recipe_id)
        user_id = get_jwt_identity()
        # 2. DB에서 삭제한다
        try:
            connection = get_connection()
            query = '''delete from recipe
                    where user_id =%s and id =%s;'''
            record = (user_id,recipe_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result': 'success','error':str(e) }
        return {'result': 'success'}
        # 3. 결과를 응답한다



class RecipeListResource(Resource):
    @jwt_required()
    def post(self) : # 내가 새롭게 만드는 함수가아니라 상속받은 Resource에있는 함수다(flask만든사람이 만든것)
        
#         {
#     "name": "김치찌개",
#     "description": "맛있게 끓이는 방법",
#     "num_of_servings": 4,
#     "cook_time": 30,
#     "directions": "고기볶고 김치넣고 물붓고 두부넣고",
#     "is_publish": 1
# }




        # 포스트로 요청한 것을 처리하는 코드 작성을 우리가!
        # 1. 클라이언트가 보낸 데이터를 받아온다.
        data = request.get_json()
        # 1-1. 헤더에 담긴 JWT 토큰 받아온다.
        user_id = get_jwt_identity() # 헤더토큰에서 user_id 뽑아준다
        print(data)
        # 2. DB에 저장한다.
        try:
            # 2-1. 데이터베이스를 연결한다.
            connection = get_connection()

            # 2-2. 쿼리문 만든다
            ###### 중요! 컬럼과 매칭되는 데이터만 %s로 바꿔준다.
            query = '''insert into recipe
                    (name,description,num_of_servings,cook_time,directions,is_publish,user_id)
                    values
                    (%s,%s,%s,%s,%s,%s,%s);'''
            #2-3. 쿼리에 매칭되는 변수 처리! 중요! 튜플로 처리해준다!(튜프은 데이터변경이 안되니까?)
            # 위의 %s부분을 만들어주는거다
            record = (data['name'], data['description'], 
                      data['num_of_servings'],data['cook_time'],data['directions'],data['is_publish'],user_id)
            #2-4 커서를 가져온다
            cursor = connection.cursor()
            #2-5 쿼리문을,커서로 실행한다.
            cursor.execute(query,record)
            #2-6 DB 반영 완료하라는, commit 해줘야한다.
            connection.commit()
            #2-7. 자원해제
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            return {'result':'fail','error': str(e)}, 500
            # 상태코드 에러에 맞게 내가 설계한다
        # 에러나면 클라이언트한테 에러났다고 알려준다
        # 3. 에러가 났으면, 에러가 났다고 알려주고, 그렇지 않으면, 잘 저장되었다고 알려준다.
    # 서버 재실행, 포스트맨에서 POST부분 send하고 mysql에서 데이터 잘 들어갔는지 확인한다
        return{'result': 'success'} # JSON방식으로해야함 하지만 쓰는 언어는 파이썬으라 여기선 ''쓴다
    def get(self):
        # 1.클라이언트로 부터 데이터를 받아온다
        # 2.저장된 레시피 리스트를 DB로부터 가져온다
        # 2-1. DB 커넥션
        try:
            connection = get_connection()
            # 2-2. 쿼리문 만든다.
            query = '''select r.*,u.username
                    from recipe r
                    join user u
                        on r.user_id = u.id
                    where is_publish = 1;'''
            # 2-3. 변수 처리할 부분은 변수처리한다.
            # 2-3. 커서 가져온다
            cursor = connection.cursor(dictionary= True)
            # 2-4. 쿼리문을 커서로 실행한다.
            cursor.execute(query)
            # 2-5. 실행 결과를 가져온다.
            result_list = cursor.fetchall()
            print(result_list)
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result': 'fail','error': str(e)},500
        # 3.데이터 가공이 필요하면 가공 후 클라이언트에 응답한다
        i = 0
        for row in result_list :
        # row는 딕셔너리 형태
            result_list[i]['createdAt']=row['createdAt'].isoformat() # 문자열로 만드는 것
            result_list[i]['updatedAt']=row['updatedAt'].isoformat()
            i = i + 1
        return {'result':'success',
                'count':len(result_list),
                'items':result_list}

# class 클래스이름(상속하는클래스)