from datetime import datetime


def data_to_patch(data):

    setattr(data, 'last_visit', datetime.utcnow())
    setattr(data, 'visits', data.visits + 1)

    return data

def integrity_err_returns(i, data):
    if 'leads_email_key' in i.__str__():
            return {'error': f'{data["email"]} already registered on database'}, 409
    if 'leads_phone_key' in i.__str__():
        return {'error': f'{data["phone"]} already registered on database'}, 409