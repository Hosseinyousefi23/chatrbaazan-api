try:
    from .local_settings import *
except (ImportError, FileNotFoundError):
    from .default_settings import *
