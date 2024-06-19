# src/__init__.py

import os

# Package-level constants or configurations can be set here
PACKAGE_NAME = "starcom_security"

# Ensure logs directory exists
if not os.path.exists("../logs"):
    os.makedirs("../logs")