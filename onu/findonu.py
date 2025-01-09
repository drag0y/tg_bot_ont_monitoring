import subprocess
import sqlite3

from pon.huawei_onu import HuaweiGetOnuInfo

class FindOnu:
    """
    Класс для поиска ОНУ, и определения состояния
    """
    def __init__(self, useronu, pon_type, snmp_com, pathdb):

        self.useronu = useronu
        self.pon_type = pon_type
        self.snmp_com = snmp_com
        self.pathdb = pathdb
        
        # ---- Подключение к базе и поиск ONU

        conn = sqlite3.connect(self.pathdb)
        cursor = conn.cursor()
        if pon_type == "epon":
            findonu = cursor.execute(f'select * from epon where maconu glob "{useronu}"')
        if pon_type == "gpon":
            findonu = cursor.execute(f'select * from gpon where snonu glob "{useronu}"')

        for onuinfo in findonu:
            self.portid = onuinfo[2]
            self.onuid = onuinfo[3]
            self.olt_ip = onuinfo[4]
            self.olt_name = onuinfo[5]    

        ponportonu = cursor.execute(f'SELECT ponport FROM ponports WHERE oltip="{self.olt_ip}" AND portoid="{self.portid}";')
             
        self.portonu_out = "Не удалось определить порт"
        for portonu in ponportonu:
            self.portonu_out = portonu[0]

        conn.close()

        self.onu_params = {
                "hostname": self.olt_name,
                "pon_type": self.pon_type,
                "olt_ip": self.olt_ip,
                "portoid": self.portid,
                "onuid": self.onuid,
                "snmp_com": self.snmp_com,
                "pathdb": self.pathdb,
                }


    def surveyonu(self):
            # ---- Состояние ОНУ

        onu_info = HuaweiGetOnuInfo(**self.onu_params)
        onu_state = onu_info.getonustatus()


        # ---- Если ONU в сети, то для опроса вызываем следующие функции
        if onu_state == '1':
            onustate = "В сети"
            level_onu, level_olt = onu_info.getonulevel() # Уровень сигнала
            outinformation = (f"""ONU найдена на OLTе: {self.olt_name}
Порт: {self.portonu_out} id: {self.onuid}

Состояние ONU: {onustate}
Статус LAN порта: {onu_info.getlanstatus()}
Статус CATV порта: {onu_info.getcatvstate()}
Время включения: {onu_info.getonuuptime()}
Время последнего отключения: {onu_info.gettimedown()}
Причина последнего отключения: {onu_info.getlastdown()}
Уровень сигнала с ОЛТа:  {level_onu}
Уровень сигнала с ОНУ:   {level_olt}
""")

        # ---- Если ONU не в сети, то вызываем следующие фуункции
        elif onu_state == '2':
            onustate = "Не в сети"
            outinformation = (f"""ONU найдена на OLTе: {self.olt_name}
Порт: {self.portonu_out} id: {self.onuid}

Состояние ONU: {onustate}
Время отключения: {onu_info.gettimedown()}
Причина отключения: {onu_info.getlastdown()}
""")
        # ---- Если состояние ONU определить не удалось
        else:
            outinformation = f"Состояние ONU: Не удалось определить {onu_state}"

        return outinformation



    def surveytreelevel(self):
        onu_info = HuaweiGetOnuInfo(**self.onu_params)
        outinformation = onu_info.getleveltree()
    
        return outinformation

    def surveytree(self):
        onu_info = HuaweiGetOnuInfo(**self.onu_params)
        outinformation = onu_info.getstatustree()

        return outinformation

