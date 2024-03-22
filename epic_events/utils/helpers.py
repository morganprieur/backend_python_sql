

def test_fct(): 
    var = 'test function' 
    print(var) 
    return var 


# Exemple 
# def jwt_required_gcp(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         id_token = request.headers['Authorization'].split(' ').pop()
#         claims = google.oauth2.id_token.verify_firebase_token(
#             id_token, HTTP_REQUEST)
#         if not claims:
#             return 'Unauthorized', 401
#         return fn(*args, **kwargs)
#     return wrapper

