
import os 
import sentry_sdk 

# import this 
from controller import Controller 
from datetime import datetime 
import sys 

sentry_sdk.init( 
    dsn=os.environ.get("SENTRY"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
) 
# from sentry_sdk import capture_message 
# capture_message('Something went wrong') 

# def main(mode='pub'): 
def main(): 

    print(f'hello main (datetime : {datetime.now()})') 

    mode = str(sys.argv[1]) 
    if not (sys.argv[2]): 
        role = None 
    else: 
        role = str(sys.argv[2]) 
    # Test Sentry 
    # division_by_zero = 1 / 0 
    # capture_message('Something went wrong') 
    controller = Controller(role) 
    controller.start(mode) 


if __name__ == "__main__": 
    """ Calls the programm with 'python project.py <mode> <role>', 
        where <mode> is the way to get the user's connection informations, 
        and <role> the role of a "demo" user. 
        Args: 
            mode (str): 'dev' NOT SECURE, get one predefined user's informations, 
                        'pub' SECURE, asks for the user's informations. 
            role (str): 'admin', 'sales' or 'support' roles. 
    """ 
    main() 

