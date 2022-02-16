import re
from flask import jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from werkzeug.exceptions import NotFound

from app.models.exceptions_model import InvalidEmail, InvalidKeys, InvalidPhone, InvalidValueType
from app.models.leads_model import Leads_Model
from app.services.helpers import data_to_patch, integrity_err_returns

def create_leads():
    data = request.get_json()
    phone_regex = "^(\([0-9]{2}\))([0-9]{5})-([0-9]{4})$"
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    try:
        if type(data['name']) != str or type(data['email']) != str or type(data['phone']) != str:
            raise InvalidValueType

        if not re.fullmatch(phone_regex, data['phone']):
            raise InvalidPhone
        
        if not re.fullmatch(email_regex, data['email']):
            raise InvalidEmail

        new_leads = Leads_Model(**data)

        current_app.db.session.add(new_leads)
        current_app.db.session.commit()

        return jsonify(new_leads), 201
    
    except InvalidValueType as ivt:
        return ivt.description, ivt.code

    except IntegrityError as i:
        return integrity_err_returns(i, data)
    
    except InvalidPhone as ip:
        return ip.description, ip.code
    
    except InvalidEmail as ie:
        return ie.email_err_description(data['email']), ie.code
    
    except KeyError as ke:
        return {"error": f'{ke.args[0]} missing'}, 400

def get_leads():
    try:
        leads = Leads_Model.query.order_by(Leads_Model.visits.desc()).all()

        if len(leads) == 0:
            raise NotFound
        

        return jsonify(leads), 200

    except NotFound:
        return {'error': 'No data found on database'}, 404

def patch_leads():
    data = request.get_json()
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    try:
        email = data['email']

        if len(data.keys()) > 1:
            raise InvalidKeys
        
        if type(email) != str:
            raise InvalidValueType

        if not re.fullmatch(email_regex, email):
            raise InvalidEmail

        query = Leads_Model.query.filter_by(email=email).one()

        data_to_patch(query)

        current_app.db.session.add(query)
        current_app.db.session.commit()

        return '', 204
    
    except KeyError as ke:
        return {"error": f'{ke.args[0]} missing'}, 400

    except NoResultFound:
        return {'error': f'{data["email"]} does not exist on database'}, 404

    except InvalidKeys as ik:
        return ik.description, ik.code
    
    except InvalidValueType as ivt:
        return ivt.description, ivt.code

    except InvalidEmail as ie:
        return ie.email_err_description(data['email']), ie.code
    

def delete_leads():
    data = request.get_json()
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    try:
        email = data['email']

        if len(data.keys()) > 1:
            raise InvalidKeys
        
        if type(email) != str:
            raise InvalidValueType

        if not re.fullmatch(email_regex, email):
            raise InvalidEmail

        query = Leads_Model.query.filter_by(email=email).one()

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204

    except NoResultFound:
        return {'error': f'{data["email"]} does not exist on database'}, 404
    
    except InvalidKeys as ik:
        return ik.description, ik.code
    
    except InvalidValueType as ivt:
        return ivt.description, ivt.code

    except InvalidEmail as ie:
        return ie.email_err_description(data['email']), ie.code
    
    except KeyError as ke:
        return {"error": f'{ke.args[0]} missing'}, 400