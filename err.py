import logging

def log_error(e):
    print(e)
    logging.error(f'{e} - Exiting with error code 2.')
    exit(2)