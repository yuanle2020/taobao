import pymysql

# mysql
mysql_host = '127.0.0.1'  # 数据库的ip地址,如果链接本地的数据库 localhost/127.0.0.1
mysql_port = 3306  # 登录数据库的用户名
mysql_user = 'root'  # 当前登录用户对应的密码
mysql_passwd = 'root'  # 数据库的端口号  默认端口号是3306
mysql_charset = 'utf8'  # 指定编码
# mysql_table = "taobao"  # 指定表名
# ----------------------------------------------------------
mysql_db = 'table1'  # 指定要链接哪个库  前提是连接的库在mysql中已经存在


# ----------------------------------------------------------


def save_mysql(res_list, mysql_table):
    L_itemId = []
    db = pymysql.connect(host=mysql_host,
                         user=mysql_user,
                         password=mysql_passwd,
                         port=mysql_port,
                         database=mysql_db,
                         charset=mysql_charset,
                         )
    cursor = db.cursor()
    try:
        # 判断是否存在此表
        cursor.execute(f"desc {mysql_table}")
    except:
        # 不存在则建表
        sql = f"""CREATE TABLE {mysql_table} (
                            itemName  VARCHAR(128),
                            itemId  VARCHAR(128),
                            categoryId VARCHAR(128),
                            auctionTags TEXT,
                            dsrScore VARCHAR(128),
                            dsrGap VARCHAR(128),
                            monthSellCount VARCHAR(128),
                            realPostFee VARCHAR(128),
                            provcity VARCHAR(128),
                            price VARCHAR(128),
                            promotionPrice VARCHAR(128),
                            sellerId VARCHAR(128),
                            sellerNickName VARCHAR(128),
                            url TEXT,
                            creativeTitle VARCHAR(128),
                            isTmall VARCHAR(128),
                            pic VARCHAR(128),
                            shopTitle VARCHAR (128))"""
        cursor.execute(sql)
        db.commit()

    for i in res_list:

        sql = f"""INSERT INTO {mysql_table}  VALUES ("{i["itemName"]}", "{i["itemId"]}", "{i["categoryId"]}", "{",".join(i["auctionTags"].split(",")[:10])}", "{i["dsrScore"]}", 
                                                "{i["dsrGap"]}", "{i["monthSellCount"]}", "{i["realPostFee"]}", "{i["provcity"]}", "{i["price"]}", "{i["promotionPrice"]}", "{i["sellerId"]}", 
                                                "{i["sellerNickName"]}","{i["url"]}", "{i["creativeTitle"]}", "{i["isTmall"]}", "{i["pic"]}", "{i["shopTitle"]}")""".replace("'",'’')
        cursor.execute(sql)
        db.commit()
        L_itemId.append((i['itemId'], i['sellerId'], i['isTmall']))

    cursor.close()
    db.close()
    return L_itemId



