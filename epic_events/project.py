
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
    # Test Sentry 
    # division_by_zero = 1 / 0 
    # capture_message('Something went wrong') 
    controller = Controller() 
    controller.start(mode) 


if __name__ == "__main__": 
    """ Call the programm with 'python project.py <arg>', 
        where <arg> is the way to get the user's connection informations. 
        Args choice: 
            'dev': NOT SECURE, get one predefined user's informations. 
            'pub': SECURE, asks for the user's informations. 
    """ 
    main() 

