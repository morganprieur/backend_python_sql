
import bcrypt 
import jwt 

# def test_fct(): 
#     var = 'test function' 
#     print(var) 
#     return var 

# décorateur qui vérifie le mdp avant de créer un utilisateur 
def jwt_gestion(fn): 
    @wraps(fn) 
    def wrapper(*args, **kwargs): 
        token = manager.verify_token(connectEmail, connectPass, connectDept) 
        if token: 
            print('deco token ok') 
        else: 
            print('deco token NOT ok') 
        return fn(*args, **kwargs) 
    return wrapper 

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

