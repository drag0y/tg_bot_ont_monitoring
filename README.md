Телеграм бот для для опроса OLT Huawei и вывода информации об абонентских терминалах.\
[Обзор функционала на Хабре](https://habr.com/ru/articles/873134/)

Есть ещё WEB версия [OLTsHUB](https://github.com/drag0y/olts_hub). У неё более широкий функционал и поддерживаются ОЛТ BDCOM.

## Установка
Клонировать репозиторий в любую удобную директорию.
Установить необходимые модули из файла requirements.txt.
```
pip install -r requirements.txt
```
Далее заполнить данные для работы.

В файле __.env__ написать токен для Телеграм Бота.
```python
TOKEN=77777:99999999
```
В файле __configurations/tgbotconf.py__ 

```python
USERS = [
        555555555,
                ]
pathdb = 'onulist.db'
snmp_com = ""
```
пишем список id пользователей которым разрешён доступ к боту, путь до базы (бот её создаст сам при опросе ОЛТов), и SNMP community.

В файле __configurations/nb_conf.py__ заполнить данные для подключения к NetBox.

```
headers = {"Authorization": ""} # Токен для NetBox
epon_tag = "" # Таг для Epon OLTов в НетБоксе
gpon_tag = "" # Таг для Gpon OLTов в НетБоксе
urlnb = "netbox.example.ru" # URL до НетБокса
```

В NetBox необходимо создать теги для Epon и Gpon и привязать их нужным ОЛТам, которые необходимо "опрашивать".\
Так же в NetBox необходимо создать платформу и привзать к ОЛТам, в данном случае платформа должна содержать слово "huawei", так бот понимает, что перед ним huawei.

## Если нету NetBox
В файле __handlers/user_private.py__ закоментировать строку
```python
from handlers.getoltlist import get_netbox_olt_list
```

и раскоментировать
```python
from handlers.not_netbox import get_netbox_olt_list
```

После этого заполнить файл __handlers/olst.py__ своими ОЛТами и можно пользоваться без нетбокса.


