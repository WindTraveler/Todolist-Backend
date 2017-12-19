from flask import session,json
from main.models import User
from flask.views import MethodView
from flask import make_response, request
from hashlib import md5
import json


salt_value = 'Ecm6'

#logout
class LogoutAPI(MethodView):

    def get(self):

        session.pop('userid', None)
        info = {
            "success": True,
            "errorMsg": False,
            "data": None
        }
        result = json.dumps(info, ensure_ascii=False)
        response = make_response(result)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


def create_md5(pwd,salt):

    md5_obj = md5()
    value = pwd + salt
    md5_obj.update(value.encode("utf8"))
    return md5_obj.hexdigest()


#登录
class LoginAPI(MethodView):

    def post(self):

        #获取前端发送的数据
        user_info = request.json
        username = user_info["username"]
        pwd = user_info["pwd"]
        sql = 'SELECT * FROM users WHERE user_name = %s;'
        parm = (username,)
        rows = User().get_User(sql, parm)

        #用户不存在
        if rows is None:
            info = {
                "success": False,
                "errorMsg": "The user doesn't exist.",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response

        # 密码错误
        md5 = create_md5(pwd, salt_value)
        if username == rows[1] and md5 != rows[2]:
            info = {
                "success": False,
                "errorMsg": "Password is wrong.",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response

        # 密码正确
        md5 = create_md5(pwd, salt_value)
        if username == rows[1] and md5 == rows[2]:
            session['userid'] = rows[0]
            info = {
                "success": True,
                "errorMsg": False,
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response


#注册
class RegisterAPI(MethodView):

    def post(self):

        #注册用户
        new_user = request.json
        username = new_user["username"]
        pwd = new_user["pwd"]

        #查询用户是否已存在
        sql = 'SELECT * FROM users WHERE user_name = %s;'
        parm = (username,)
        rows = User().get_User(sql, parm)

        #若用户已存在，返回错误信息
        if rows is not None:
            info = {
                "success": False,
                "errorMsg": "The email has been registered.",
                "data": None
            }

        #用户注册
        else:
            md5 = create_md5(pwd, salt_value)
            sql_add = 'INSERT INTO users (user_name,pwd_hash) VALUES (%s,%s);'
            parm_add = (username, md5)
            User().set_User(sql_add, parm_add)
            info = {
                "success": True,
                "errorMsg": False,
                "data": None,
            }

        result = json.dumps(info, ensure_ascii=False)
        response = make_response(result)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
