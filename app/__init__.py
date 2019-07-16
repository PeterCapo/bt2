# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            shortcode = int(request.data.get('shortcode', ''))
            msisdn = int(request.data.get('msisdn', ''))
            commandid = str(request.data.get('commandid', ''))
            billrefnumber = str(request.data.get('billrefno', ''))
            refno = str(request.data.get('refno', ''))
            if name and shortcode and msisdn and commandid and billrefnumber and refno:
                bucketlist = Bucketlist(name=name, shortcode=shortcode, msisdn=msisdn, commandid=commandid, billrefnumber=billrefnumber, refno=refno)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'shortcode': bucketlist.shortcode,
                    'msisdn': bucketlist.msisdn,
                    'commandid': bucketlist.commandid,
                    'billrefnumber': bucketlist.billrefnumber,
                    'refno': bucketlist.refno
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified,
                    'shortcode': buckelist.shortcode,
                    'msisdn': buckelist.msisdn,
                    'commandid': buckelist.commandid,
                    'billrefnumber': buckelist.billrefnumber,
                    'refno': buckelist.refno
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
            # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
                "message":
                "bucketlist {} deleted successfully".format(bucketlist.id)
                 }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            shortcode = int(request.data.get('shortcode', ''))
            msisdn = int(request.data.get('msisdn', ''))
            commandid = str(request.data.get('commandid', ''))
            billrefno = str(request.data.get('billrefno', ''))
            refno = str(request.data.get('refno', ''))
            bucketlist.name = name
            buckelist.shortcode = shortcode
            buckelist.msisdn = msisdn
            buckelist.commandid = commandid
            buckelist.billrefno = billrefno
            buckelist.refno = refno
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'shortcode': buckelist.shortcode,
                'msisdn': buckelist.msisdn,
                'commandid': buckelist.commandid,
                'billrefno': buckelist.billrefno,
                'refno': buckelist.refno
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified,
                'shortcode': buckelist.shortcode,
                'msisdn': buckelist.msisdn,
                'commandid': buckelist.commandid,
                'billrefno': buckelist.billrefno,
                'refno': buckelist.refno
            })
            response.status_code = 200
            return response

    return app
