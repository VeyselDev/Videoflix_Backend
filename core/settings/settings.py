import os
import sys

ENV = os.environ.get('ENV')

if ENV == 'dev':
    from core.settings.dev import *
elif ENV == 'prod':
    from core.settings.prod import *
else:
    sys.stderr.write(f"Error: Invalid ENV value '{ENV}'. Must be 'dev' or 'prod'.\n")
    sys.exit(1)

if not SECRET_KEY:
    sys.stderr.write("Error: SECRET_KEY environment variable not set.\n")
    sys.exit(1)

if not ALLOWED_HOSTS and ENV == 'prod':
    sys.stderr.write("Error: ALLOWED_HOSTS environment variable not set in production.\n")
    sys.exit(1)