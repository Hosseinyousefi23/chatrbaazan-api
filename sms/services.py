import requests


def send_verification_sms(user, request=None, text=None, mobile=None, verify_code=1):
    """
    sending verification sms via post method
    :param appointment:
    :param request:
    :return:        validate_phone(request.POST.get('phone', ''))

    """
    url_post = 'http://smspanel.Trez.ir/SendMessageWithPost.ashx'
    if text is None:
        text = "کد تاییدیه:{***REMOVED*** با تشکر چتربازان".format(verify_code)
    params = {
        'UserName': 'Vahidsaadat1',
        'Password': 'vma#123',
        'PhoneNumber': '50002237242500',
        'MessageBody': text,
        'RecNumber': mobile,
        'Smsclass': '1',
    ***REMOVED***

    r = requests.post(url_post, data=params)
    print(r.url)
    print(r.status_code)
    print(r.text)
    return r.status_code
