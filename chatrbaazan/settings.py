"""
Django settings for chatrbaazan project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import datetime
import os
from chatrbaazan.env import ENV


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


def _(s): return s


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-1i*lwg9euwv7$avo6@j-214s9ed@flzh$(-*5@y@_mlo=d!x7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV['DEBUG']

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'contact',
    'carts',
    'like',
    'emm',
    'about',
    'accounts',
    'sms',
    'rest_framework',
    'rest_auth',
    'rest_auth.registration',
    'django.contrib.sites',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'rest_framework.authtoken',

]
# CKEDITOR_BASEPATH = "/public/assets/ckeditor/ckeditor"
# CKEDITOR_JQUERY_URL = STATIC_ROOT + '/js/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "editor/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': [
                'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']***REMOVED***,
            {'name': 'clipboard', 'items': [
                'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']***REMOVED***,
            {'name': 'editing', 'items': [
                'Find', 'Replace', '-', 'SelectAll']***REMOVED***,
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']***REMOVED***,
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']***REMOVED***,
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']***REMOVED***,
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']***REMOVED***,
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']***REMOVED***,
            '/',
            {'name': 'styles', 'items': [
                'Styles', 'Format', 'Font', 'FontSize']***REMOVED***,
            {'name': 'colors', 'items': ['TextColor', 'BGColor']***REMOVED***,
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']***REMOVED***,
            {'name': 'about', 'items': ['About']***REMOVED***,
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]***REMOVED***,
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] ***REMOVED***],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    ***REMOVED***
***REMOVED***
# end config edit
LOGIN_REDIRECT_URL = "/"
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
USERNAME_FIELD = 'email'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CORS_ORIGIN_ALLOW_ALL = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatrbaazan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        ***REMOVED***,
    ***REMOVED***,
]

WSGI_APPLICATION = 'chatrbaazan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
SITE_ID = 1
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     ***REMOVED***
# ***REMOVED***
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV['DBNAME'],
        'USER': ENV['USERDB'],
        'PASSWORD': ENV['PASSWORDDB'],
        'HOST': ENV['HOST'],
        'PORT': ENV['PORT'],
    ***REMOVED***
***REMOVED***
# Configure the JWTs to expire after 1 hour, and allow users to refresh near-expiration tokens
JWT_AUTH = {

    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3000),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',

***REMOVED***

# Enables django-rest-auth to use JWT tokens instead of regular tokens.

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    ***REMOVED***,
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    ***REMOVED***,
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    ***REMOVED***,
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    ***REMOVED***,
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public/assets')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/assets'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '')

# Rest Framework configurations
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
***REMOVED***
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'accounts.serializers.RegisterSerializerCustom',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
    'LOGIN_SERIALIZER': 'accounts.serializers.LoginSerializer',
***REMOVED***
LOGIN_SERIALIZER= 'accounts.serializers.LoginSerializer',

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
    'LOGIN_SERIALIZER': 'accounts.serializers.LoginSerializer',
***REMOVED***
REST_AUTH_REGISTER_PERMISSION_CLASSES = (
    ('accounts.permissions.AllowAnyAnonymous'),
)
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
AUTH_USER_MODEL = 'accounts.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
REST_USE_JWT = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# Config django-jet
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    ***REMOVED***,
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    ***REMOVED***,
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    ***REMOVED***,
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    ***REMOVED***,
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    ***REMOVED***,
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    ***REMOVED***
]
'''
Adds buttons to change forms that allows you to navigate to previous/next 
object without returning back to change list. Can be disabled if hit performance.
'''
JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'
JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'

# SMTP Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mohammad.chavoshipor@gmail.com'
EMAIL_HOST_PASSWORD = 'soxftfkswnndhnkf'

# Cart Debug
CART_DEBUG = ENV['CART_DEBUG'] if ENV['CART_DEBUG'] else False
URI_FRONT = ENV['URI_FRONT'] if ENV['URI_FRONT'] else 'http://0.0.0.0:4200/'
