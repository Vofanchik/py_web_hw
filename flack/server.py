import atexit
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, EmailStr, validator, ValidationError
import re

engine = create_engine('sqlite:///users.db', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())

PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

class HttpError(Exception):

    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

class UserCreateModel(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def strong_password(cls, value):
        if not PASSWORD_REGEX.match(value):
            raise ValueError('password too easy')
        return value




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    reg_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)

app = Flask('server')
bcr = Bcrypt(app)

@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.error_message
    })
    response.status_code = error.status_code
    return response

@app.errorhandler(ValidationError)
def validation_error_handler(error: ValidationError):
    response = jsonify({
        'error': error.errors()
    })
    response.status_code = 400
    return response

class UserView(MethodView):
    def get(self):
        pass

    def post(self):
        json_data = request.json
        json_data_validated = UserCreateModel(email=json_data['email'], password=json_data['password']).dict()
        with Session() as session:
            user = User(email=json_data_validated['email'], password=bcr.generate_password_hash(
                json_data_validated['password'].encode()).decode()
                        )
            session.add(user)
            try:
                session.commit()
                return jsonify({
                    'id': user.id,
                    'reg_time': user.reg_time.isoformat()
                })
            except:
                raise HttpError(400, 'user already exists')


# @flask.route('/test/', methods=['POST'])
# def test():
#     json_data = request.json
#     headers = request.headers
#     qs = request.args
#
#     return jsonify({'status':'ok',
#                     'json_data': json_data,
#                     'headers': dict(headers),
#                     'qs': dict(qs)})

app.add_url_rule('/users/', view_func=UserView.as_view('create_user'), methods=['POST'])

app.run(
    host='0.0.0.0',
    port=5000
)
