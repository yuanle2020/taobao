import pymongo

# mongoDB
host = '127.0.0.1'
port = 27017
set_name = "taobao_comment"


def save_mongoDB(comments_list, table_name):
    # 连接mongDB数据库
    client = pymongo.MongoClient(host=host, port=port)
    db = client[set_name]
    if comments_list:
        id = 'comment_id' if comments_list[0].get('comment_id') else 'rateId'
        for c in comments_list:
            # 数据入库
            db[table_name].update({id: c[id]}, {'$set': dict(c)}, True)
