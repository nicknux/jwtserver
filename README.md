# JWT Server

## Running Locally

### REST API
```
$ python3 main.py
```

## Commands

### Adding a new client

Auto-generated client_id, client_secret, and client_key
```
python3 adduser <CLIENT_NAME>
```

Migrating existing client_id, client_secret, and client_key
```
python3 adduser <CLIENT_NAME> --id <CLIENT_ID> --secret <CLIENT_SECRET> --key <CLIENT_KEY> --salt <SALT_USED>
```
