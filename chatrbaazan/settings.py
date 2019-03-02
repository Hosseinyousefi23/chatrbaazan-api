try:
    from .local_settings import *
except ImportError or FileNotFoundError:
    from .default_settings import *
