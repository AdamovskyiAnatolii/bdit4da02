import sys
from typing import Dict


def error_info(e: Exception) -> Dict[str, str]:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    err = {
        'type': str(exc_type.__name__),
        'text': str(exc_obj),
    }
    return err
