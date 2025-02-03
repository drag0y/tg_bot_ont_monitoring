headers = {"Authorization": ""} # Токен для NetBox
epon_tag = "" # Таг для Epon OLTов в НетБоксе
gpon_tag = "" # Таг для Gpon OLTов в НетБоксе
urlnb = "" #
urlgetepon = f"{urlnb}/api/dcim/devices/?q=&tag={epon_tag}" # URL что бы вытягивать список Epon OLTов
urlgetgpon = f"{urlnb}/api/dcim/devices/?q=&tag={gpon_tag}" # URL что бы вытягивать список Gpon OLTов
