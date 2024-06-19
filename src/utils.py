# src/utils.py

import logging
import os
import configparser

# Set up logging
def setup_logging(log_file='app.log'):
    if not os.path.exists('../logs'):
        os.makedirs('../logs')
    
    logging.basicConfig(
        filename=os.path.join('../logs', log_file),
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    logging.info('Logging setup complete.')

# Read configuration from a file
def read_config(config_file='config/config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

# Write configuration to a file
def write_config(config, config_file='config/config.ini'):
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Utility to log events
def log_event(event):
    logging.info(event)

# Utility to log errors
def log_error(error):
    logging.error(error)