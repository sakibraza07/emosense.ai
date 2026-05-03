from flask import request, jsonify
from functools import wraps
import jwt
from config import JWT_SECRET

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            # Decode the token
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user_id = payload["user_id"]
            request.user_email = payload["email"]
            # Token is valid, proceed
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function