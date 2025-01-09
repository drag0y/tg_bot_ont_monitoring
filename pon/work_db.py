import sqlite3


class WorkDB:
    def __init__(self, pathdb):
        self.pathdb = pathdb
       

    def createnewdb(self):
        conn = sqlite3.connect(self.pathdb)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS epon")
        cursor.execute("DROP TABLE IF EXISTS gpon")
        cursor.execute("DROP TABLE IF EXISTS ponports")
        cursor.execute("CREATE TABLE epon(number integer primary key autoincrement, maconu, portonu text, idonu text, oltip, oltname)")
        cursor.execute("CREATE TABLE gpon(number integer primary key autoincrement, snonu, portonu text, idonu text, oltip, oltname)")
        cursor.execute("CREATE TABLE ponports(number integer primary key autoincrement, oltip text, oltname text, ponport text, portoid text)")
        conn.close()


    def finddoublemac(self):

        outdoublemac2 = []
        nl = '\n'

        conn = sqlite3.connect(self.pathdb)
        cursor = conn.cursor()

        dubleonu = cursor.execute('select maconu, count(*) from epon group by maconu having count(*) > 1')
        dublicatemac = []
        dublicatemac2 = []

        for row in dubleonu:
            dublicatemac.append(row[0])

        if dublicatemac:
            for row in dublicatemac:
                macdoubleonu = cursor.execute(f'select * from epon where maconu glob "{row}"')
                for row in macdoubleonu:
                    outdoublemac2.append(row[1] + " " + row[4])
            outdoublemac = f"Повторяющиеся ONU на EPON OLTах: {nl}{nl.join(outdoublemac2)}"

        else:
            outdoublemac = "\nНа OLTах EPON нет повторяющихся ОНУ"
        
        conn.close()

        return outdoublemac


    def finddoublesn(self):

        outdoublesn2 = []
        dublicatesn = []
        dublicatesn2 = []
        nl = '\n'

        conn = sqlite3.connect(self.pathdb)
        cursor = conn.cursor()

        dubleonusn = cursor.execute('select snonu, count(*) from gpon group by snonu having count(*) > 1')

        for row in dubleonusn:
            dublicatesn.append(row[0])

        if dublicatesn:
            for row in dublicatesn:
                sndoubleonu = cursor.execute(f'select * from gpon where snonu glob "{row}"')
                for row in sndoubleonu:
                    outdoublesn2.append(row[1] + " " + row[4])
            outdoublesn = f"Повторяющиеся ONU на GPON OLTах: {nl}{nl.join(outdoublesn2)}"

        else:
            outdoublesn = "\nНа OLTах GPON нет повторяющихся ОНУ"

        conn.close()

        return outdoublesn
