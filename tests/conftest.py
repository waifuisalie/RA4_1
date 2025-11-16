import sys
import os

# Add project root to Python path for all tests
# This allows imports like: from src.RA3.functions.python import tipos
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
