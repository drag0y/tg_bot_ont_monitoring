import requests
import json
import ipaddress
import sqlite3

from pon.work_db import WorkDB
from configurations.tgbotconf import pathdb, snmp_com
from pon.huawei_olt import HuaweiGetOltInfo
from configurations.nb_conf import urlgetepon, urlgetgpon, epon_tag, gpon_tag, headers


def get_netbox_olt_list():
# --- Функция опрашивает NetBox по тегам, создаёт БД, обнуляя старую если есть.
# --- И дальше передаёт данные об ОЛТе в другие функции для опроса

    out_epon_olts = []
    out_gpon_olts = []

    epon = "epon"
    gpon = "gpon"


    # --- Создание базы, если база существует, то старая удаляется
    db = WorkDB(pathdb)
    db.createnewdb()


# --- Получениие списка Epon ОЛТов, если такие есть, то передаём их в функцию snmpgetonu 

    if epon_tag:
        response = requests.get(urlgetepon, headers=headers, verify=False)
        olts_list = json.loads(json.dumps(response.json(), indent=4))

        for parse_olts_list in olts_list["results"]:
            olt_name = []
            olt_addr = []
            olt_name = parse_olts_list["name"]
            olt_addr = ipaddress.ip_interface(parse_olts_list["primary_ip4"]["address"])
            olt_ip = str(olt_addr.ip)
            platform = parse_olts_list["platform"]["name"]

            out_epon_olts.append(olt_name + " " + olt_ip)

            if "huawei" in platform:
                get_olt = HuaweiGetOltInfo(olt_name, olt_ip, snmp_com, pathdb, epon)
                get_olt.getonulist()
                get_olt.getoltports()
           

# --- Получение списка Gpon ОЛТов, если такие есть, то передаём их в функцию snmpgetonu 

    if gpon_tag:
        response = requests.get(urlgetgpon, headers=headers, verify=False)
        olts2_list = json.loads(json.dumps(response.json(), indent=4))

        for parse_olts_list in olts2_list["results"]:
            olt_name = []
            olt_addr = []
            olt_name = parse_olts_list["name"]
            olt_addr = ipaddress.ip_interface(parse_olts_list["primary_ip4"]["address"])
            olt_ip = str(olt_addr.ip)
            platform = parse_olts_list["platform"]["name"]
            
            out_gpon_olts.append(olt_name + " " + olt_ip)

            if "huawei" in platform:
                get_olt = HuaweiGetOltInfo(olt_name, olt_ip, snmp_com, pathdb, gpon)
                get_olt.getonulist()
                get_olt.getoltports()

# --- Поиск одинаковых Маков в базе
    
    outdoublemac = db.finddoublemac()

# --- Поиск одинаковых серийников в базе

    outdoublesn = db.finddoublesn()


    return outdoublemac, outdoublesn, out_epon_olts, out_gpon_olts


