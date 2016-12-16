from config import loader
from configuration import DbConfiguration
from datetime import datetime
from models import *

import argparse
import base64
import bcrypt
import random
import sqlalchemy.exc
import uuid

"""
Initialize parser
"""
parser = argparse.ArgumentParser()
parser.add_argument('name', help='Name of client')
parser.add_argument('--id', help='client_id to use')
parser.add_argument('--secret', help='client_secret to use')
parser.add_argument('--key', help='client_key to use')
parser.add_argument('--salt', help='Salt to use for hashing the secret')
args = parser.parse_args()

"""
Initialize DB session
"""
service_dbengine = DbConfiguration.getengine(
    *DbConfiguration.get_service_config('jwtserver'))
service_dbsession = DbConfiguration.newsession(service_dbengine)

"""
Get arg values
"""
name = args.name
client_id = args.id or uuid.uuid4().__str__()
client_secret = args.secret or base64.standard_b64encode(
    bytes(str(random.getrandbits(256)), 'utf-8')).decode('utf-8')
client_key = args.key or base64.standard_b64encode(
        bytes(uuid.uuid4().__str__(), 'utf-8')).decode('utf-8')

"""
Get Salt
"""
if args.salt == None:
    encsalt = bcrypt.gensalt(4)
else:
    salt = args.salt
    encsalt = bytes("$2a$12$%s" % salt, 'utf-8')

"""
Hash secret
"""
hashedsecret = bcrypt.hashpw(bytes(client_secret, 'utf-8'), salt=encsalt)

"""
Save to DB
"""
try:
    client = Client(name=name, client_id=client_id,
                    client_secret=hashedsecret, client_key=client_key,
                    create_date=datetime.utcnow(),
                    update_date=datetime.utcnow())
    service_dbsession.add(client)
    service_dbsession.commit()
    client.client_secret = client_secret
    print(client)
except sqlalchemy.exc.IntegrityError as e:
    print(e)

