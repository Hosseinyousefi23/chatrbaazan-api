try:
    from .local_settings import *
except FileNotFoundError:
    from .default_settings import *
