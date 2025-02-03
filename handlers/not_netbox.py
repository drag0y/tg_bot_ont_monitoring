import requests
import json
import ipaddress
import sqlite3

from pon.work_db import WorkDB
from configurations.tgbotconf import pathdb, snmp_com
from handlers.olst import olts
from pon.huawei_olt import HuaweiGetOltInfo


def get_netbox_olt_list():


    # --- Создание базы, если база существует, то старая удаляется
    db = WorkDB(pathdb)
    db.createnewdb()


# --- Получениие списка Epon ОЛТов, если такие есть, то передаём их в функцию snmpgetonu 

    out_epon_olts = []
    out_gpon_olts = []

    for olts_list in olts:
        olt_name = olts[olts_list]["olt_name"]
        olt_ip = olts[olts_list]["olt_ip"]
        pon = olts[olts_list]["pon"]

        if pon == "epon":
            out_epon_olts.append(olt_name + " " + olt_ip)
            get_olt = HuaweiGetOltInfo(olt_name, olt_ip, snmp_com, pathdb, pon)
            get_olt.getonulist()
            get_olt.getoltports()
           
        elif pon == "gpon":
            out_gpon_olts.append(olt_name + " " + olt_ip)
            get_olt = HuaweiGetOltInfo(olt_name, olt_ip, snmp_com, pathdb, pon)
            get_olt.getonulist()
            get_olt.getoltports()

# --- Поиск одинаковых Маков в базе
    
    outdoublemac = db.finddoublemac()

# --- Поиск одинаковых серийников в базе

    outdoublesn = db.finddoublesn()

    return outdoublemac, outdoublesn, out_epon_olts, out_gpon_olts


