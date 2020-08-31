# test-vk-auth
Данный проект был релизован для тестового задания простой авторизации через ВКонтакте.

# Настройка виртуального окружения.
1. Создать виртуальное окружение Python3.7 virtualenv.
```
pip install virtualenv
```
2. Установить зависимости.
```
pip install -r requirements.txt
```
# Настройка авторизации через ВКонтакте.
1. Создать файл vk_client.py в папке проекта vk_auth_project.
2. Записать в vk_client.py данные приложения в ВК для доступа к VK API.
```
CLIENT_ID = '12345'
CLIENT_SECRET_CODE = 'abcdef'
```
# Запуск.
```
python manage.py runserver <addrport>
```
