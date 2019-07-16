# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Payment
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/payments/', methods=['POST', 'GET'])
    def payments():
        if request.method == "POST":
            amount = str(request.data.get('amount', ''))
            shortcode = int(request.data.get('shortcode', ''))
            msisdn = int(request.data.get('msisdn', ''))
            commandid = str(request.data.get('commandid', ''))
            billrefnumber = str(request.data.get('billrefno', ''))
            refno = str(request.data.get('refno', ''))
            if amount and shortcode and msisdn and commandid and billrefnumber and refno:
                payment = Payment(amount=amount,
                                  shortcode=shortcode, msisdn=msisdn,
                                  commandid=commandid,
                                  billrefnumber=billrefnumber, refno=refno)
                payment.save()
                response = jsonify({
                    'id': payment.id,
                    'amount': payment.amount,
                    'date_created': payment.date_created,
                    'date_modified': payment.date_modified,
                    'shortcode': payment.shortcode,
                    'msisdn': payment.msisdn,
                    'commandid': payment.commandid,
                    'billrefnumber': payment.billrefnumber,
                    'refno': payment.refno
                })
                response.status_code = 201
                return response
        else:
            # GET
            payments = Payment.get_all()
            results = []

            for payment in payments:
                obj = {
                    'id': payment.id,
                    'amount': payment.amount,
                    'date_created': payment.date_created,
                    'date_modified': payment.date_modified,
                    'shortcode': payment.shortcode,
                    'msisdn': payment.msisdn,
                    'commandid': payment.commandid,
                    'billrefnumber': payment.billrefnumber,
                    'refno': payment.refno
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/api/payments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def payment_manipulation(id, **kwargs):
            # retrieve a payment using it's ID
        payment = Payment.query.filter_by(id=id).first()
        if not payment:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            payment.delete()
            return {
                "message":
                "payment {} deleted successfully".format(payment.id)
                 }, 200

        elif request.method == 'PUT':
            amount = str(request.data.get('amount', ''))
            shortcode = int(request.data.get('shortcode', ''))
            msisdn = int(request.data.get('msisdn', ''))
            commandid = str(request.data.get('commandid', ''))
            billrefno = str(request.data.get('billrefno', ''))
            refno = str(request.data.get('refno', ''))
            payment.amount = amount
            payment.shortcode = shortcode
            payment.msisdn = msisdn
            payment.commandid = commandid
            payment.billrefnumber = billrefnumber
            payment.refno = refno
            payment.save()
            response = jsonify({
                'id': payment.id,
                'amount': payment.amount,
                'date_created': payment.date_created,
                'date_modified': payment.date_modified,
                'shortcode': payment.shortcode,
                'msisdn': payment.msisdn,
                'commandid': payment.commandid,
                'billrefnumber': payment.billrefnumber,
                'refno': payment.refno
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': payment.id,
                'amount': payment.amount,
                'date_created': payment.date_created,
                'date_modified': payment.date_modified,
                'shortcode': payment.shortcode,
                'msisdn': payment.msisdn,
                'commandid': payment.commandid,
                'billrefnumber': payment.billrefnumber,
                'refno': payment.refno
            })
            response.status_code = 200
            return response

    return app
