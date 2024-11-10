from functools import wraps
from flask import request, jsonify
from firebase_admin import auth

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # Get the Firebase token from the request headers
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401

        try:
            # Verify the Firebase token
            auth.verify_id_token(token.split()[1])
            return func(*args, **kwargs)
        except auth.ExpiredIdTokenError:
            return jsonify({'error': 'TOKEN_EXPIRED'}), 401
        except auth.InvalidIdTokenError:
            return jsonify({'error': 'Unauthorized'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated
