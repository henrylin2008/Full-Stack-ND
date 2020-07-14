from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

app = Flask(__name__)

AUTH0_DOMAIN = 'dev-wmig32c8.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'myapp'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split() # split the auth part
    if parts[0].lower() != 'bearer': # if first index is not 'bearer', raise 401
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1: 
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1] # header part 
    return token 


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read()) # body of json file, array of keys 
                               # {'keys': [{'alg': 'RS256',
                               # 'kty': 'RSA',
                               # 'use': 'sig',
                               # 'x5c': [adsfasf]
                               # 'kid': 'NzgyRTVDRjJCQkRBRDcwN0QxRTA1OUIyRTNFODAxOTc0Njc5OTJEOA',}]}
    unverified_header = jwt.get_unverified_header(token) # unpack jwt header and verify the kid id in the header, and validate
    # {'typ': 'JWT',
    # 'alg': 'RS256',
    # 'kid': 'NzgyRTVDRjJCQkRBRDcwN0QxRTA1OUIyRTNFODAxOTc0Njc5OTJEOA'}
    rsa_key = {}
    if 'kid' not in unverified_header: # if 'kid' not in the header, raise 401 error 
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']: # if 'kid' in jwks
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key: # if we have rsa_key
        try:
        # USE THE KEY TO VALIDATE THE JWT
        # {'iss': 'https://fsnd.auth0.com/',
        # 'sub': 'auth0|5d03d3e6726b8f0cb4bf71c9',
        # 'aud': 'image',
        # 'iat': 1560556174,
        # 'exp': 1560563374,
        # 'azp': 'ki4B6jZkuJd87bpB2Mw8zdkj1l3ofpzj',
        # 'scope': '',
        # 'permissions': ['get:images', 'post:images']}
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


def check_permissions(permission, payload):
    if 'permissions' not in payload: # ensure payload contains 'permissions' key 
        abort(400)
    if permission not in payload['permissions']: # if permission exists in payload['permissions'] array 
        abort(403)
    return True


def requires_auth(permission=''): # single permission string, default to empty string 
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator


@app.route('/headers')
@requires_auth('get:images')
def headers(payload):
    print(payload)
    return 'Access Granted'
