
import sentry_sdk
sentry_sdk.init(
    dsn="https://92f2fd7678cf64d3efff193b8390cc2e@o4506970696646656.ingest.us.sentry.io/4506970703200256",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
) 
# import this 
from controller import Controller 
from datetime import datetime 


def main(mode='pub'): 

    print(f'hello main {datetime.now()}') 
    # Test Sentry 
    # division_by_zero = 1 / 0 
    controller = Controller() 
    controller.start(mode) 


if __name__ == "__main__": 
    # main('pub') 
    main('dev') 

