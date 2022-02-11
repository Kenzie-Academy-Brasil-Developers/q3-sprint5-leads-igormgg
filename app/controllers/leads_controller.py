import re
from flask import jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import NoResultFound

from app.models.exceptions_model import InvalidEmail, InvalidPhone
from app.models.leads_model import Leads_Model
from app.services.helpers import data_to_patch, integrity_err_returns

    # print('*'*100)
    # print(query.visits)
    # print('*'*100)

def create_leads():
    data = request.get_json()
    phone_regex = "^(\([0-9]{2}\))([0-9]{5})-([0-9]{4})$"
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    try:
        if not re.fullmatch(phone_regex, data['phone']):
            raise InvalidPhone
        
        if not re.fullmatch(email_regex, data['email']):
            raise InvalidEmail

        new_leads = Leads_Model(**data)

        current_app.db.session.add(new_leads)
        current_app.db.session.commit()

        return jsonify(new_leads), 201

    except IntegrityError as i:
        return integrity_err_returns(i, data)
    
    except InvalidPhone as ip:
        return ip.description, ip.code
    
    except InvalidEmail as ie:
        return ie.email_err_description(data['email']), ie.code

def get_leads():
    try:
        leads = Leads_Model.query.all()

        if len(leads) == 0:
            raise NotFound
        

        return jsonify(leads), 200

    except NotFound:
        return {'error': 'No data found on database'}, 404

def patch_leads(email):
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    try:
        if not re.fullmatch(email_regex, email):
            raise InvalidEmail

        query = Leads_Model.query.filter_by(email=email).one()

        data_to_patch(query)

        current_app.db.session.add(query)
        current_app.db.session.commit()

        return '', 204
    
    except NoResultFound:
        return {'error': f'{email} does not exist on database'}, 404

    except InvalidEmail as ie:
        return ie.email_err_description(email), ie.code

def delete_leads(email):
    # data = request.get_json()

    try:
        query = Leads_Model.query.filter_by(email=email).one()

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204

    except NoResultFound:
        return {'error': f'{email} does not exist on database'}, 404