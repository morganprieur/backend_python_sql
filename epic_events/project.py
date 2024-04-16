
import os 
import sentry_sdk 

# import this 
from controller import Controller 
from datetime import datetime 

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

def main(mode='pub'): 

    print(f'hello main {datetime.now()}') 
    # Test Sentry 
    # division_by_zero = 1 / 0 
    # capture_message('Something went wrong') 
    controller = Controller() 
    controller.start(mode) 


if __name__ == "__main__": 
    # main('pub') 
    main('dev') 

