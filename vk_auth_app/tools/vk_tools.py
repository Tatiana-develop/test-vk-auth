import logging

from django.conf import settings
from urllib.parse import urlparse
from requests import get

from vk_auth_app.tools.sessionhandler import get_session_key


logger = logging.getLogger('django')


class VkApi:
    client_id = settings.OAUTH_VK['client_id']
    display = settings.OAUTH_VK['display']
    scope = settings.OAUTH_VK['scope']
    response_type = settings.OAUTH_VK['response_type']
    client_secret_code = settings.OAUTH_VK['client_secret_code']
    version = settings.OAUTH_VK['v']
    authorize_url = settings.OAUTH_VK['authorize_url']
    main_url_methods = settings.VK_API_METHODS['url']
    vk_api_methods = settings.VK_API_METHODS['methods']

    def __init__(self, request):
        session_values = get_session_key(request, 'member_id', 'access_token')
        if session_values:
            self.member_id = session_values[0]
            self.access_token = session_values[1]
        else:
            self.redirect_uri = self.get_redirect_uri(request)

    def get_url_authorize(self):

        if self.redirect_uri:
            vk_oauth_url = '{authorize_url}?client_id={client_id}&display={display}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}&v={version}'.format(
                authorize_url=self.authorize_url,
                client_id=self.client_id,
                display=self.display,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
                response_type=self.response_type,
                version=self.version
            )
            return vk_oauth_url
        else:
            logging.warning('AttributeError: class VkOauth don\'t has a request parameter')
            raise AttributeError('class VkOauth don\'t has a request parameter')

    def get_friends(self):
        get_friend_method = self.vk_api_methods['get_friends']
        name_method = get_friend_method['name_method']

        params_string = self.get_params_to_string(get_friend_method)
        url_get_friend = '{main_url_methods}{name_method}?user_id={user_id}{params}&access_token={access_token}&v={version}'.format(
            main_url_methods=self.main_url_methods,
            name_method=name_method,
            user_id=self.member_id,
            params=params_string,
            access_token=self.access_token,
            version=self.version
        )
        response = get(url_get_friend).json()['response']['items']
        return response

    def get_info_user(self):
        get_users_method = self.vk_api_methods['get_users']
        name_method = get_users_method['name_method']
        params_string = self.get_params_to_string(get_users_method)
        url_get_info = '{main_url_methods}{name_method}?user_id={user_id}{params_string}&access_token={access_token}&v={version}'.format(
            main_url_methods=self.main_url_methods,
            name_method=name_method,
            user_id=self.member_id,
            params_string=params_string,
            access_token=self.access_token,
            version=self.version
        )
        try:
            response = get(url_get_info).json()['response'][0]
            return response
        except:
            logger.warning('Error with get_user\'s_info request')

    def get_token(self, code):
        url = 'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={secret}&redirect_uri={redirect_uri}&code={code}'.format(
            client_id=self.client_id,
            secret=self.client_secret_code,
            redirect_uri=self.redirect_uri,
            code=code
        )

        response = get(url).json()

        if 'access_token' in response.keys() and 'user_id' in response.keys():
            access_token = response['access_token']
            user_id = response['user_id']
        else:
            access_token = ''
            user_id = ''
        return access_token, user_id

    @staticmethod
    def get_redirect_uri(request):
        absolute_uri = request.build_absolute_uri()
        redirect_path = settings.OAUTH_VK['redirect_path']
        absolute_uri_parse = urlparse(absolute_uri)
        redirect_uri = '{scheme}://{netloc}/{path}'.format(
            scheme=absolute_uri_parse.scheme,
            netloc=absolute_uri_parse.netloc,
            path=redirect_path)
        return redirect_uri

    @staticmethod
    def get_params_to_string(params_dict):
        params_string = ''
        for key, value in params_dict.items():
            if key == 'name_method':
                continue
            params_string += '&{key}={value}'.format(key=key, value=value)
        return params_string
