import atexit
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, EmailStr, validator, ValidationError
import re

engine = create_engine('sqlite:///advertisement.db', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())


class HttpError(Exception):

    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message


class Advertisment(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    reg_time = Column(DateTime, server_default=func.now())
    author = Column(String, nullable=False)


Base.metadata.create_all(engine)

app = Flask('server')

@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.error_message
    })
    response.status_code = error.status_code
    return response


class AdverView(MethodView):
    def get(self):
        def serialize(ad):
            return {
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'author': ad.author,
                'reg_time' : ad.reg_time
            }
        with Session() as session:
            advert = session.query(Advertisment).all()
            try:
                session.commit()
                return jsonify([serialize(a) for a in advert])

            except:
                pass

    def post(self):
        json_data = request.json
        with Session() as session:
            advert = Advertisment(title=json_data['title'], description=json_data['description'], author=json_data['author'])
            session.add(advert)
            try:
                session.commit()
                return jsonify({
                    'id': advert.id,
                    'reg_time': advert.reg_time.isoformat(),
                    'title': advert.title
                })
            except:
                raise HttpError(400, 'some error')

    def delete(self, adv_id):
        json_data = request.json
        with Session() as session:
            advert = session.query(Advertisment).get({adv_id})
            # session.add(advert)
            try:
                session.commit()
                return jsonify({
                    'id': advert.id,
                    'reg_time': advert.reg_time.isoformat(),
                    'title': advert.title
                })
            except:
                pass



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

app.add_url_rule('/advertisment/', view_func=AdverView.as_view('create_adver'), methods=['POST', 'GET', 'DELETE'])
app.run(
    host='0.0.0.0',
    port=5000
)
