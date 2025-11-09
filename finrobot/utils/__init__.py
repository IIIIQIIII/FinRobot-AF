"""
Utility modules for FinRobot-AF.
"""

from .data_loader import (
    TenKDataLoader,
    ResultWriter,
    load_10k_item7,
    list_available_filings
)

# Import from parent utils.py module
# This is needed because Python prioritizes utils/ package over utils.py module
import sys
import os
_parent_dir = os.path.dirname(os.path.dirname(__file__))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Now import from finrobot.utils module (the .py file, not this package)
import importlib.util
_utils_py_path = os.path.join(os.path.dirname(__file__), '..', 'utils.py')
_spec = importlib.util.spec_from_file_location("_finrobot_utils_module", _utils_py_path)
_utils_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_utils_module)

# Re-export commonly used functions from utils.py
decorate_all_methods = _utils_module.decorate_all_methods
save_output = _utils_module.save_output
SavePathType = _utils_module.SavePathType
get_current_date = _utils_module.get_current_date
get_next_weekday = _utils_module.get_next_weekday

__all__ = [
    'TenKDataLoader',
    'ResultWriter',
    'load_10k_item7',
    'list_available_filings',
    'decorate_all_methods',
    'save_output',
    'SavePathType',
    'get_current_date',
    'get_next_weekday',
]
