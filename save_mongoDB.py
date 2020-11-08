import pymongo

# mongoDB
host = '127.0.0.1'
port = 27017
set_name = "taobao"


def save_mongoDB(res_list,table_name):
    L_itemId = []
    client = pymongo.MongoClient(host=host, port=port)
    db = client[set_name]

    for i in res_list:
        db[table_name].update({'itemId': i['itemId']},{'$set':dict(i)},True)
        print(i)
        L_itemId.append((i['itemId'], i['sellerId'], i['isTmall']))

    return L_itemId

