from flask import Flask
from view.users import *
from view.notes import *


app = Flask(__name__)
app.secret_key = '123'


app.add_url_rule('/logout','logout',logout)

#login/register
user_view = UserAPI.as_view('user_api')
app.add_url_rule('/login/api/users/', view_func=user_view, methods=['POST'])
rgs_view = RegisterAPI.as_view('rgs_api')
app.add_url_rule('/register/api/users/', view_func=rgs_view, methods=['POST'])

#todos
note_view = NoteAPI.as_view('note_api')
app.add_url_rule('/api/todos/', view_func=note_view, methods=['GET','POST','PUT','DELETE'])

# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#haha

if __name__ == '__main__':
    app.run(debug=True)
