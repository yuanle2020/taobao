import os, csv


def save_csv(res_list, csv_file_name):
    L_itemId = []

    path = 'csv/'
    # 判断\新建文件夹
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, ' 文件夹创建成功')
    file_name = path + csv_file_name
    # 判断\新建文件
    if not os.path.exists(file_name):
        header = ["itemName", "itemId", "shopTitle", "categoryId", "auctionTags", "dsrScore",
                  "dsrGap", "monthSellCount",
                  "realPostFee", "pic", "provcity", "url", "promotionPrice", "sellerId", "sellerNickName", "price",
                  "creativeTitle", "isTmall"]
        with open(file_name, 'a', newline='', encoding='ansi') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    # 写入文件
    for item in res_list:
        with open(file_name, 'a', newline='', encoding='ansi') as f:
            L_itemId.append(item["itemId"])
            writer = csv.writer(f)
            L = [item["itemName"], item["itemId"], item["shopTitle"], item["categoryId"],
                 item["auctionTags"], item["dsrScore"], item["dsrGap"], item["monthSellCount"],
                 item["realPostFee"], item["pic"], item["provcity"], item["url"], item["promotionPrice"], item["sellerId"],
                 item["sellerNickName"], item["price"], item["creativeTitle"], item["isTmall"]]
            writer.writerow(L)

    return L_itemId