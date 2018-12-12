import requests


def send_verification_sms(user, request=None, text=None, mobile=None):
    """
    sending verification sms via post method
    :param appointment:
    :param request:
    :return:
    """
    url_post = 'http://smspanel.Trez.ir/SendMessageWithPost.ashx'
    if text is None:
        text = text.replace("{VERIFIYCODE***REMOVED***", str(user.verify_code))
    mobile_number = user.phone if user.user is None else user.user
    params = {
        'UserName': 'Sepandteb',
        'Password': 'sepandteb1132',
        'PhoneNumber': '50005858997',
        'MessageBody': text,
        'RecNumber': mobile_number,
        'Smsclass': '1',
    ***REMOVED***

    r = requests.post(url_post, data=params)
    print(r.url)
    print(r.status_code)
    print(r.text)
    return r.status_code
