import sys
from pathlib import Path
import pytest

# Find the actual project folder
PROJECT_ROOT = Path.cwd()

if not (PROJECT_ROOT / "src" / "diagnose.py").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent

# Import the actual diagnostic module
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from diagnose import diagnose, load_models, parse_parameters
