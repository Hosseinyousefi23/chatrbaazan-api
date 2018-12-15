### step1: Create virtualenv
```$xslt
virtualenv -p /usr/bin/python3.6 venv
```
* clone project backend
### Build Project
```$xslt
pip install -r package.txt
```

### Requirements
```$xslt
python 3.6
```

### Config For Jet Dashboard
```$xslt
python manage.py migrate jet
python manage.py migrate dashboard
python manage.py collectstatic

```

apt install libpq-dev