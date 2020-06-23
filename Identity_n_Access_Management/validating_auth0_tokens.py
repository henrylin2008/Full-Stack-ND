# Install a pip package in the current Jupyter kernel
# import sys
# !{sys.executable} -m pip install python-jose

import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'dev-wmig32c8.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'myapp'
# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVKN3Judll2aFZqTC0tV3VTLUJCdCJ9.eyJpc3MiOiJodHRwczovL2Rldi13bWlnMzJjOC51cy5hdXRoMC5jb20vIiwic3ViIjoiNktveWlaMXBmMjRNZ1g1V29VWldwOGNoU1lqVlFxYlZAY2xpZW50cyIsImF1ZCI6Im15YXBwIiwiaWF0IjoxNTkyOTIyOTg5LCJleHAiOjE1OTMwMDkzODksImF6cCI6IjZLb3lpWjFwZjI0TWdYNVdvVVpXcDhjaFNZalZRcWJWIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.bd6vr70mNYIPLyfiRvq9Y1rmJftK3KDy8PTyW8rLZ7omgyN0BIn5JR_71heaoV_js4-g0pxm_Yslwvt-9jmB1o-jv35ZkX8l17ZiI0-CkoCAPeVxvh12uCNoVXVAjoTFJDpO8S_n9JhWUaPi5m4yuSsVlcRFUoA-za1n80P8Bb734vaa3gw4LtDU4kqfg5yBtVX-O3aWe6gfZjQtLfqQghZV9dfh44akMF-TRAw0RZc1fw4QvqIMymySJ2EEjt-s-C-SSDutSfHun-89_x5JKhU2J3jCWIXZISNPyxr_b-fIiEbEi_iLM9O9v1GM1sSeqh_SVhlLv80_NqZ_rBVglA"

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
	# print(jwks)
	# {
	# 	'keys': [
	# 	{
	# 		'alg': 'RS256', 
	# 		'kty': 'RSA', 
	# 		'use': 'sig', 
	# 		'n': 'uJB681mfc68WDpcfUd07T63kfOaqxJ4-dA3i0wFxGPzeJnb0nvLYoWuv1lBBC6_dVA_X5J4uNKreu5l1XoT7c_3LKbfNBjia1qOzm9HKm0j4HUkOOt-UU2_g-111Pqg17uy3zeKtKBm_ZsAloJP6k6S7WZ_zlhuklYdGdvMO3spSXgb3yXP2hCDA3onWAAHKEORH7KYZ-pie7VMojOWL7UZ_5sPobrRQ-rtYzykHffaDMsldbaj0_elWzfAS6-SR8OKhOjw3nZC9KeVuyrtHhPpEn5wgqO45CVSXN4A0v5rV_Gr9ile7y13TjQ66W_QAYuo_O6bWMo1IDrCEauRhiw', 
	# 		'e': 'AQAB', 
	# 		'kid': 'eJ7rnvYvhVjL--WuS-BBt', 
	# 		'x5t': 'nEWS7AD-krU9a0OGu2iK1iCOSHk', 
	# 		'x5c': ['MIIDDTCCAfWgAwIBAgIJTmt2kJwy41iyMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi13bWlnMzJjOC51cy5hdXRoMC5jb20wHhcNMjAwNjIyMTcwMzIzWhcNMzQwMzAxMTcwMzIzWjAkMSIwIAYDVQQDExlkZXYtd21pZzMyYzgudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuJB681mfc68WDpcfUd07T63kfOaqxJ4+dA3i0wFxGPzeJnb0nvLYoWuv1lBBC6/dVA/X5J4uNKreu5l1XoT7c/3LKbfNBjia1qOzm9HKm0j4HUkOOt+UU2/g+111Pqg17uy3zeKtKBm/ZsAloJP6k6S7WZ/zlhuklYdGdvMO3spSXgb3yXP2hCDA3onWAAHKEORH7KYZ+pie7VMojOWL7UZ/5sPobrRQ+rtYzykHffaDMsldbaj0/elWzfAS6+SR8OKhOjw3nZC9KeVuyrtHhPpEn5wgqO45CVSXN4A0v5rV/Gr9ile7y13TjQ66W/QAYuo/O6bWMo1IDrCEauRhiwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQmTCE9KiOCfpTxZe+yehvunVaOLDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKjUH4ooLBFnYpf9oin4yeBbxuyaEy14Tdebe9V0RWwEeuNrjhWqxjUNiqzdVNKLlAk9Dhrujha2ACqcT/FN0iowxH4WmF6A7fFMbukvINf7H+m5LbTwhA0PUEJEbZgiOqSHJ44DWxmNigEkI1FqeVBzHy63seQRqcS9Lzt+TlQnLjcoGIaEkPR2qXi4dX0XAhiwnEfb19sn+ia526y/cZLO0PBK/XKRQKR2GNEoS0Y7w2HXxdMeQELo7FtidBjc1IdyuNNi8V+Vgwc2TO/EFp3riHZNwwieebQjsEUdux94KJQclRdFeqh1uK1BuuTV2bkLqrLkeaFq+UQf/48+Elk=']
	# 	}, 
	# 	{	
	# 		'alg': 'RS256', 
	# 		'kty': 'RSA', 
	# 		'use': 'sig', 
	#		'n': 'mJkH8zwRXQx7DDokK3ATBwXaiL9O5qNGtlFDF823ewRaFb2DTlW2MhqucmGqWiD0nh5ddedOTVGKwxYAUvgFO2pUEk_u8Ro9HfYUUaV8rjpPPvmcYTmF0emCZDFPbEpuDCdzfG57vCi0pJ-ruLEn33m0C35pbwZJ1H77MCS8E1149JwWhQSIXAuN5zLRHDx_AjqjtRfgT3xxsgJyd5zS1G4g0FnVLtTxmLzcc9IUnzP-huQ8ZJwXBhhFlO0-BCSkqgOlh8JZbS9xjJbdcWEov7hbstLPkv2Ar4KXchtPC0zaP9S8ojKfb01DwEY_Z_f5vvt5Z8GmG6blbs3QlHSB3w', 
	# 		'e': 'AQAB', 
	# 		'kid': 'AV3M_6hoHGt4yDf6miTaf', 
	# 		'x5t': 'AXX4YihZ2Hlb1NKhLJ5XR06tfbk', 
	# 		'x5c': ['MIIDDTCCAfWgAwIBAgIJcS+Y9SGri88lMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi13bWlnMzJjOC51cy5hdXRoMC5jb20wHhcNMjAwNjIyMTcwMzIzWhcNMzQwMzAxMTcwMzIzWjAkMSIwIAYDVQQDExlkZXYtd21pZzMyYzgudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmJkH8zwRXQx7DDokK3ATBwXaiL9O5qNGtlFDF823ewRaFb2DTlW2MhqucmGqWiD0nh5ddedOTVGKwxYAUvgFO2pUEk/u8Ro9HfYUUaV8rjpPPvmcYTmF0emCZDFPbEpuDCdzfG57vCi0pJ+ruLEn33m0C35pbwZJ1H77MCS8E1149JwWhQSIXAuN5zLRHDx/AjqjtRfgT3xxsgJyd5zS1G4g0FnVLtTxmLzcc9IUnzP+huQ8ZJwXBhhFlO0+BCSkqgOlh8JZbS9xjJbdcWEov7hbstLPkv2Ar4KXchtPC0zaP9S8ojKfb01DwEY/Z/f5vvt5Z8GmG6blbs3QlHSB3wIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5+ZNqSo2gIxNBBUHa4nvC1r+bnzAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBABvRXEhoizxD7iVvh9oGupMw1hwfIXv7O786ek1IOue43QV3wTH5C50WuLXaZsD57V8akkqMV83GlP79nJyq1V9sewQqX581fHjUhzKYY/MTE56N4vkRz4kjVhgXbpR3bD7XUfOrJw6Gg7cRXOqj+KgzbjDwbP2T15EqoM99ftVccqBnR1TD1xSOrd7gSc3Ege/n19Iz0jnQlWAtGiH9mHHjsAfcYc54exkD7f/2GgOpPMLpqn1OWrZgjcFDRev0ojwqVKYtazvP1WNJVL0FmPANQxm0c+rrY8KumnkA0MRV04ucEXPv7po7L6zeWBuXL9igkc5kidvJBwJFs4n9X6Y=']
	# 	}
	#	]
	# }
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
	# print(unverified_header):    
   	# {'alg': 'RS256', 'typ': 'JWT', 'kid': 'eJ7rnvYvhVjL--WuS-BBt'}

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
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