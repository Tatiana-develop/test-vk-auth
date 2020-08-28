import logging

from django.shortcuts import render, HttpResponseRedirect
from urllib.parse import urlparse, parse_qsl

from vk_auth_app.tools.sessionhandler import get_session_key, set_session_key, remove_session
from vk_auth_app.tools.vk_tools import VkApi


logger = logging.getLogger('django')


def home(request):
    logger.info('In home page')
    if get_session_key(request, 'member_id'):
        vkapi = VkApi(request)
        friends_list = vkapi.get_friends()
        friends = [{'name': get_pretty_name(friend), 'photo': friend['photo_100']} for friend in friends_list]
        friends = [friends[i:i+3] for i in range(0, len(friends), 3)]
        user_info = vkapi.get_info_user()
        name_user = get_pretty_name(user_info)
        return render(request, 'home.html', {
            'friends': friends,
            'user_name': name_user
        })
    else:
        vk_oauth_url = VkApi(request).get_url_authorize()

        return render(request, 'home.html', {
            'vk_oauth_url': vk_oauth_url
        })


def login(request):
    logger.info('login view')
    current_url = request.get_full_path()
    url_query = urlparse(current_url).query
    url_params = dict(parse_qsl(url_query))
    if 'code' in url_params.keys():
        access_token, user_id = VkApi(request).get_token(code=url_params['code'])
        if access_token and user_id:
            set_session_key(request, member_id=user_id, access_token=access_token)
            return HttpResponseRedirect('/')
        else:
            logger.warning('token is not founded.')
    else:
        logger.warning('Code is not found.')
        return HttpResponseRedirect('/')
    return render(request, 'home.html')


def logout(request):
    remove_session(request)
    return HttpResponseRedirect('/')


def get_pretty_name(user_info):
    return user_info['last_name'] + ' ' + user_info['first_name']
