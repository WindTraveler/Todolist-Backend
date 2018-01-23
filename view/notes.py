from flask import session,json
from main.models import Note
from flask.views import MethodView
from flask import make_response, request
import json


class NoteAPI(MethodView):

    def get(self):

        if session.get('userid') is not None:
            masterid = session.get('userid')

            # 获用户所有note数据
            sql = 'SELECT * FROM notes WHERE user_id = %s AND deleted = False ORDER BY note_id DESC;'
            parm = (masterid,)
            rows = Note().get_AllNote(sql, parm)
            # 读取元组数据，转换为json类型
            notes = []
            for row in rows:
                note = {}
                note['id'] = row[0]
                note['content'] = row[1]
                note['completed'] = row[2]
                note['deleted'] = row[3]
                notes.append(note)

            #返回所有notes信息
            info = {
                "success": True,
                "errorMsg": None,
                "data": notes
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        else:

            # 未登录，返回错误信息
            info = {
                "success": False,
                "errorMsg": "Please log in first!",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response


    def post(self):

        print(request.cookies.get("userid"))
        if session.get('userid') is not None:
            masterid = session.get('userid')

            # 获取前端发送的note内容
            new_note = request.json
            content = new_note["content"]

            # 添加一条note
            sql_add = 'INSERT INTO notes (content,completed,deleted,user_id) VALUES (%s,FALSE,FALSE ,%s);'
            parm_add = (content, masterid)
            Note().set_Note(sql_add, parm_add)

            # 获用户添加的note的id
            sql = 'SELECT * FROM notes WHERE user_id = %s ORDER BY note_id DESC;'
            parm = (masterid,)
            newnote = Note().get_Note(sql, parm)

            # 获用户添加的note数据
            sql = 'SELECT * FROM notes WHERE note_id = %s;'
            parm = (newnote[0],)
            rows = Note().get_AllNote(sql, parm)

            # 读取元组数据，转换为json类型
            notes = []
            for row in rows:
                note = {}
                note['id'] = row[0]
                note['content'] = row[1]
                note['completed'] = row[2]
                note['deleted'] = row[3]
                notes.append(note)

            # 返回新添加的note信息
            info = {
                "success": True,
                "errorMsg": None,
                "data": notes
            }

            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        else:
            # 未登录，返回错误信息
            info = {
                "success": False,
                "errorMsg": "Please log in first!",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response


    def put(self):

        if session.get('userid') is not None:
            masterid = session.get('userid')

            # 获取前端发送的note内容
            note = request.json
            noteid =  note["id"]
            content = note["content"]
            completed = note["completed"]
            deleted = note["deleted"]

            if noteid is not None:
                # 修改note信息
                sql_update = 'UPDATE notes SET content = %s,completed = %s,deleted = %s  WHERE note_id = %s;'
                parm_update = (content,completed,deleted,noteid)
                Note().set_Note(sql_update, parm_update)

                # 获用更改后的note
                sql = 'SELECT * FROM notes WHERE note_id = %s;'
                parm = (noteid,)
                rows = Note().get_AllNote(sql, parm)

                # 读取元组数据，转换为json类型
                notes = []
                for row in rows:
                    note = {}
                    note['id'] = row[0]
                    note['content'] = row[1]
                    note['completed'] = row[2]
                    note['deleted'] = row[3]
                    notes.append(note)

                # 返回修改后的note信息
                info = {
                    "success": True,
                    "errorMsg": None,
                    "data": notes
                }

                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response
            else:
                # 返回错误信息
                info = {
                    "success": False,
                    "errorMsg": "can not find a note",
                    "data": None
                }
                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

        else:
            # 未登录，返回错误信息
            info = {
                "success": False,
                "errorMsg": "Please log in first!",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

    def options(self):
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, X-ID, X-TOKEN, X-ANY-YOUR-CUSTOM-HEADER"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT"
        return response


class DeleteAPI(MethodView):

    def put(self):

        if session.get('userid') is not None:
            masterid = session.get('userid')

            # 获取前端发送的note内容
            listid = request.json["idList"]
            if listid is not None:
                notes = []
                for id in listid:
                    # 修改note的deleted值
                    sql_update = 'UPDATE notes SET deleted = True WHERE note_id = %s;'
                    parm_update = (id,)
                    Note().set_Note(sql_update, parm_update)

                # 获取所有未删除的note
                sql = 'SELECT * FROM notes WHERE user_id = %s AND deleted = False ORDER BY note_id DESC;'
                parm = (masterid,)
                rows = Note().get_AllNote(sql, parm)

                if rows is not None:
                    # 读取元组数据，转换为json类型
                    for row in rows:
                        note = {}
                        note['id'] = row[0]
                        note['content'] = row[1]
                        note['completed'] = row[2]
                        note['deleted'] = row[3]
                        notes.append(note)

                # 返回note信息
                info = {
                    "success": True,
                    "errorMsg": None,
                    "data": notes
                }

                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

            else:
                # 返回错误信息
                info = {
                    "success": False,
                    "errorMsg": "can not find a note",
                    "data": None
                }
                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

        else:
            # 未登录，返回错误信息
            info = {
                "success": False,
                "errorMsg": "Please log in first!",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response

    def options(self):
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, X-ID, X-TOKEN, X-ANY-YOUR-CUSTOM-HEADER"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT"
        return response


class AllCompleteAPI(MethodView):

    def put(self):

        if session.get('userid') is not None:
            masterid = session.get('userid')
            #获取数据类型，确定全部完成或全部未完成
            type = request.json["type"]

            #全部设置为：已完成
            if type == "1" :
                # 修改note信息
                sql_update = 'UPDATE notes SET completed = True WHERE user_id = %s AND deleted = False;'
                parm_update = (masterid,)
                Note().set_Note(sql_update, parm_update)

                # 获用更改后的所有note
                sql = 'SELECT * FROM notes WHERE user_id = %s AND deleted = False ORDER BY note_id DESC;'
                parm = (masterid,)
                rows = Note().get_AllNote(sql, parm)

                # 读取元组数据，转换为json类型
                notes = []
                for row in rows:
                    note = {}
                    note['id'] = row[0]
                    note['content'] = row[1]
                    note['completed'] = row[2]
                    note['deleted'] = row[3]
                    notes.append(note)

                # 返回note信息
                info = {
                    "success": True,
                    "errorMsg": None,
                    "data": notes
                }

                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

            #全部设置为：未完成
            if type == "0":
                # 修改note信息
                sql_update = 'UPDATE notes SET completed = False WHERE user_id = %s AND deleted = False;'
                parm_update = (masterid,)
                Note().set_Note(sql_update, parm_update)

                # 获用更改后的所有note
                sql = 'SELECT * FROM notes WHERE user_id = %s AND deleted = False ORDER BY note_id DESC;'
                parm = (masterid,)
                rows = Note().get_AllNote(sql, parm)

                # 读取元组数据，转换为json类型
                notes = []
                for row in rows:
                    note = {}
                    note['id'] = row[0]
                    note['content'] = row[1]
                    note['completed'] = row[2]
                    note['deleted'] = row[3]
                    notes.append(note)

                # 返回note信息
                info = {
                    "success": True,
                    "errorMsg": None,
                    "data": notes
                }

                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

            else :
                # 返回错误信息
                info = {
                    "success": False,
                    "errorMsg": "value of type is wrong",
                    "data": None
                }

                result = json.dumps(info, ensure_ascii=False)
                response = make_response(result)
                response.headers["Content-Type"] = "application/json; charset=utf-8"
                response.headers["Access-Control-Allow-Origin"] = "*"
                return response

        else:
            # 未登录，返回错误信息
            info = {
                "success": False,
                "errorMsg": "Please log in first!",
                "data": None
            }
            result = json.dumps(info, ensure_ascii=False)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

    def options(self):
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, X-ID, X-TOKEN, X-ANY-YOUR-CUSTOM-HEADER"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT"
        return response