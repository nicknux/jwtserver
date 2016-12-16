# JWT Server

## Running Locally

### REST API
```
$ python3 main.py
```

## Commands

### Adding a new Client

Auto-generated client_id, client_secret, and client_key
```
$ python3 adduser <CLIENT_NAME>
```

Migrating existing client_id, client_secret, and client_key
```
$ python3 adduser <CLIENT_NAME> --id <CLIENT_ID> --secret <CLIENT_SECRET> --key <CLIENT_KEY> --salt <SALT_USED>
```

Sample output:
```
{
    name: 'TestClient',
    client_id: 'abcc7e7f-6da0-4b9b-8dd7-ef005efabcde',
    client_secret: 'MTA1NDI5NjMwNDgyNjQ5NDcxODA2NzM4MDUzOTE2MDU0NTcwNzk3ODc0NDA1Mzk5MjI0NDE0OTE0MjE4MDA3MzI3MTk2MjEyMjabcde=',
    client_key: 'NTgzY2QyNTYtMWE5MC00NDUzLTkyNzEtMzY5YTM5OGEabcde',
    create_date: '2016-12-16 18:12:48',
    update_date: '2016-12-16 18:12:48'
}
```

- You need to share the client_id, client_secret, and client_key to the owner of this Client credentials and the Service that the client will be authenticated to.

### Requesting a JSON Web Token
Example Request from Client:
```
curl -X POST -H "Content-Type: application/json" -d '{
  "client_id":"0e7b292a-b85a-41d6-b6e6-a42d029abcde",
  "client_secret":"OTIyMDM2Mjg2OTA4MDM3MDU2MjQ3NDI2MjczMjAwMTIyMzM5MTkzMDMyNDMxNzI5OTkxNDM5NDM0NDMzOTE5OTE1MDc4OTkyOTabcde=",
  "claims":"search,export"
}' "http://127.0.0.1:5001/auth"
```
Example Response:
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODE4MjkzOTYsImNsYWltcyI6InNlYXJjaCxleHBvcnQiLCJpYXQiOjE0ODE4MjIxOTYsImlzcyI6Imp3dHNlcnZlci4xLjAwIn0.vKYCPT5aTp43l3Qjdey9Rro6zEi_x-RKOPIZK6rNecA"
}
```
The Client will then need to pass the JWT to every request to the Service.

### Validating the token on the server side
You need to use PyJWT https://github.com/jpadilla/pyjwt.

On, the Service side, they would verify the JSON Web Token using the originally provided client_key as the shared secret. This client_key is unique for this Client.

Example:
```python
import jwt

service_claims = ['admin','sysadmin']
decoded_jwt = jwt.decode(
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0ODE4MjkzOTYsImNsYWltcyI6InNlYXJjaCxleHBvcnQiLCJpYXQiOjE0ODE4MjIxOTYsImlzcyI6Imp3dHNlcnZlci4xLjAwIn0.vKYCPT5aTp43l3Qjdey9Rro6zEi_x-RKOPIZK6rNecA',
    'NTgzY2QyNTYtMWE5MC00NDUzLTkyNzEtMzY5YTM5OGEabcde')

requested_claims = decoded_jwt['claims'].split(',')
if len(list(set(reqclaims) & set (svcclaims))) == 0:
    # raise an error because the requested claims are not in the claims required by the Service
    raise 'Unauthorized access'

```

