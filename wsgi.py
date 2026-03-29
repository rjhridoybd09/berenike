# ─────────────────────────────────────────────────────────────────────────────
# WSGI configuration file for PythonAnywhere
#
# IMPORTANT: Replace YOUR_USERNAME below with your actual PythonAnywhere username
# ─────────────────────────────────────────────────────────────────────────────

import sys
import os

# Add your project folder to the Python path
# Replace YOUR_USERNAME with your actual PythonAnywhere username
project_home = '/home/YOUR_USERNAME/ocr_studio'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set working directory so relative paths (like uploads/) work correctly
os.chdir(project_home)

from app import app as application
