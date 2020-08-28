import logging

from django.conf import settings


logger = logging.getLogger('django')


def set_cookie_age(request):
    request.session.set_expiry(settings.SESSION_COOKIE_AGE)


def set_session_key(request, **kwargs):
    for key, value in kwargs.items():

        if key == 'access_token':
            set_cookie_age(request)

        request.session[key] = value


def get_session_key(request, *args):
    values = list()
    request_session_keys = request.session.keys()

    for key in args:
        if key in request_session_keys:
            value = request.session[key]
            values.append(value)

    return values


def remove_session(request):
    keys = list(request.session.keys())
    if keys:
        for key in keys:
            del request.session[key]
    else:
        logger.warning('session keys are not founded.')
