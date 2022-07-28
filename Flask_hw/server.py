import atexit
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.views import MethodView

engine = create_engine('sqlite:///advertisement.db', echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())


class HttpError(Exception):

    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message


class Advertisment(Base):
    __tablename__ = 'advertisments'
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



@app.route('/advertisment/<int:adv_id>', methods=['DELETE'])
def delete(adv_id):
    with Session() as session:
        advert = session.query(Advertisment).get(adv_id)
        try:
            session.delete(advert)
            session.commit()
            return jsonify({
                'id': advert.id,
                'title': advert.title

            },{'status' : 'delete success'})
        except:
            raise HttpError(400, '''id isn't exist''')

@app.route('/advertisment/<int:adv_id>', methods=['PATCH'])
def patch(adv_id):
    json_data = request.json
    with Session() as session:
        session.query(Advertisment).filter_by(id = adv_id).update(json_data)
        try:
            session.commit()
            adver = session.query(Advertisment).get(adv_id)
            return jsonify({
                'id': adver.id,
                'title': adver.title,
                'description': adver.description,
                'author': adver.author,
            }, {'status': 'update success'})
        except:
            raise HttpError(400, '''id isn't exist''')

@app.route('/advertisment/<int:adv_id>', methods=['GET'])
def get(adv_id):
    with Session() as session:
        try:
            session.commit()
            adver = session.query(Advertisment).get(adv_id)
            return jsonify({
                'id': adver.id,
                'title': adver.title,
                'description': adver.description,
                'author': adver.author,
            })
        except:
            raise HttpError(400, '''id isn't exist''')





app.add_url_rule('/advertisment/', view_func=AdverView.as_view('create_adver'), methods=['POST', 'GET'])
app.run(
    host='0.0.0.0',
    port=5000
)
