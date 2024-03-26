
import bcrypt 
import jwt 
import functools 

# from controller import Controller 
# controller = Controller() 

# def test_fct(): 
#     var = 'test function' 
#     print(var) 
#     return var 

# # décorateur qui hashe le mdp avant de créer un utilisateur 
# def decorator_hash_pass(fn): 
#     print('helpers') 
#     @functools.wraps(fn) 
#     def wrapper(*args, **kwargs): 
#         hashed_password = hash_pw(password, nb) 
#         # hashed_password = manager.hash_pw(password, nb) 
#         print('hashed_password Helpers : ', hashed_password) 
#         # if token: 
#         #     print('deco token ok') 
#         # else: 
#         #     print('deco token NOT ok') 
#         return fn(*args, **kwargs) 
#     return wrapper 


# décorateur qui vérifie le token avant de créer un utilisateur 
def decorator_verify_jwt(fn): 
    @wraps(fn) 
    def wrapper(*args, **kwargs): 
        token = manager.verify_token(connectEmail, connectPass, connectDept) 
        print('token (helpers) : ', token) 
        # if token: 
        #     print('deco token ok') 
        # else: 
        #     print('deco token NOT ok') 
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

