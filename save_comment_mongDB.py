import pymongo

# mongoDB
host = '127.0.0.1'
port = 27017
set_name = "taobao_comment"


def save_mongoDB(comments_list,table_name):
    # 连接mongDB数据库
    client = pymongo.MongoClient(host=host, port=port)
    db = client[set_name]

    if comments_list:
        for c in comments_list:
            comment_id = c['id']
            buyer_id = c['displayUserNick']
            auction_sku = c['auctionSku']
            rate_content = c['rateContent']
            rate_date = c['rateDate']
            goods_img = c['pics']
            goods_video = c['videoList']
            cms_source = c['cmsSource']
            seller_id = c['sellerId']
            useful = c['useful']
            dic = {'comment_id': comment_id, 'buyer_id': buyer_id, 'auction_sku': auction_sku,
                   'rate_content': rate_content,
                   'rate_date': rate_date, 'goods_img': goods_img, 'goods_video': goods_video,
                   'cms_source': cms_source, 'seller_id': seller_id, 'useful': useful}

            # 数据入库
            db[table_name].update({'comment_id': dic['comment_id']}, {'$set': dict(dic)}, True)


