import base64
import json
from datetime import datetime, timedelta

import bcrypt
import hashlib
import jwt
from flask import Flask, request, jsonify

from config import loader
from models import *
from configuration import DbConfiguration

app = Flask('jwt-server')
service_dbengine = DbConfiguration.getengine(
    *DbConfiguration.get_service_config('jwtserver'))

@app.route('/auth', methods=['POST'])
def authenticate():
    body = request.data.decode('utf-8')
    creds = json.loads(body)
    pwd = bytes(creds['client_secret'], 'utf-8')
    current_config = loader.ConfigLoader().current()
    config_salt = current_config['salt']

    service_dbsession = DbConfiguration.newsession(service_dbengine)
    client = service_dbsession.query(Client).filter_by(
        client_id=creds['client_id']).first()

    # verify secret
    salt = bytes("$2a$12$%s" % config_salt, 'utf-8')
    hashedpwd = bcrypt.hashpw(pwd, salt=salt)
    secret = bytes(client.client_secret, 'utf-8')
    secret_matches = hashedpwd == secret

    if secret_matches:
        minute = timedelta(minutes=1)
        token = jwt.encode(
            {
                'claims': creds['claims'],
                'exp': datetime.utcnow() + minute * int(current_config[
                    'token_expiration_minutes']),
                'iss': current_config['issuer'],
                'iat': datetime.utcnow()
            },
            client.client_key,
            algorithm='HS256')
        return jsonify({'token': token.decode('utf-8')}), 200
    else:
        return jsonify({'error':'invalid credentials'}), 402
