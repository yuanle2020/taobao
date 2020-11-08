import requests
import hashlib
import time, os, csv, json
from urllib.parse import quote
import threading
from queue import Queue


class TaoBao:
    def __init__(self, str_searchContent, num_pageSize, num_page, appKey, threads_num_get_pages,
                 switch_save, proxies, threads_num_get_comments, taobao_comments_num):
        self.str_searchContent = str_searchContent
        self.num_pageSize = num_pageSize
        self.num_page = num_page
        self.appKey = appKey
        self.threads_num_get_pages = threads_num_get_pages
        self.threads_num_get_comments = threads_num_get_comments
        self.switch_save = switch_save
        self.proxies = proxies
        self.taobao_comments_num = taobao_comments_num
        self.cookie = ''
        self.token = ''
        self.file_name = ''
        self.L_itemId = []
        self.run()

    # 第一次请求,无cookie请求,获取cookie
    def first_requests(self):

        base_url = 'https://h5api.m.taobao.com/h5/mtop.alimama.union.sem.landing.pc.items/1.0/?jsv=2.4.0&appKey=12574478&t=1582738149318&sign=fe2cf689bdac8258a1d12507a06bd289&api=mtop.alimama.union.sem.landing.pc.items&v=1.0&AntiCreep=true&dataType=jsonp&type=jsonp&ecode=0&callback=mtopjsonp1&data=%7B%22keyword%22%3A%22%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA%22%2C%22ppath%22%3A%22%22%2C%22loc%22%3A%22%22%2C%22minPrice%22%3A%22%22%2C%22maxPrice%22%3A%22%22%2C%22ismall%22%3A%22%22%2C%22ship%22%3A%22%22%2C%22itemAssurance%22%3A%22%22%2C%22exchange7%22%3A%22%22%2C%22custAssurance%22%3A%22%22%2C%22b%22%3A%22%22%2C%22clk1%22%3A%22%22%2C%22pvoff%22%3A%22%22%2C%22pageSize%22%3A%22100%22%2C%22page%22%3A%22%22%2C%22elemtid%22%3A%221%22%2C%22refpid%22%3A%22%22%2C%22pid%22%3A%22430673_1006%22%2C%22featureNames%22%3A%22spGoldMedal%2CdsrDescribe%2CdsrDescribeGap%2CdsrService%2CdsrServiceGap%2CdsrDeliver%2C%20dsrDeliverGap%22%2C%22ac%22%3A%22%22%2C%22wangwangid%22%3A%22%22%2C%22catId%22%3A%22%22%7D'
        try:

            response = requests.get(base_url)
            get_cookies = response.cookies.get_dict()
            _m_h5_tk = get_cookies['_m_h5_tk']
            _m_h5_tk_enc = get_cookies['_m_h5_tk_enc']
            self.token = _m_h5_tk.split('_')[0]
            self.cookie = '_m_h5_tk={}; _m_h5_tk_enc={}'.format(_m_h5_tk, _m_h5_tk_enc)
        except Exception as e:
            print('first_requests 出错: ', e)

    # md5加密sign
    def sign(self, token, tme, appKey, data):
        st = token + "&" + tme + "&" + appKey + "&" + data
        m = hashlib.md5(st.encode(encoding='utf-8')).hexdigest()
        return m

    # 第二次请求，爬取商品信息
    def second_requests(self):
        # 第二次带cookie请求,返回数据并存储
        searchContent = self.str_searchContent
        pageSize = str(self.num_pageSize)  # 每页结果数
        page = str(self.num_page)  # 第几页
        str_data = '{"pNum":' + page + ',"pSize":"' + pageSize + r'","refpid":"mm_26632258_3504122_32538762","variableMap":"{\"q\":\"' + searchContent + r'\",\"navigator\":false,\"union_lens\":\"recoveryid:201_11.20.207.176_1974284_1603940990104;prepvid:201_11.20.207.176_1974284_1603940990104\",\"recoveryId\":\"201_11.92.48.12_2098594_1603960009303\"}","qieId":"36308","spm":"a2e0b.20350158.31919782","app_pvid":"201_11.92.48.12_2098594_1603960009303","ctm":"spm-url:a2e0b.20350158.search.1;page_url:https%3A%2F%2Fuland.taobao.com%2Fsem%2Ftbsearch%3Frefpid%3Dmm_26632258_3504122_32538762%26keyword%3D%25E8%25A3%25A4%25E5%25AD%2590%26clk1%3D38b36e679f3fa0d5a81bf45a4bb89d18%26upsid%3D38b36e679f3fa0d5a81bf45a4bb89d18%26spm%3Da2e0b.20350158.search.1%26pid%3Dmm_26632258_3504122_32538762%26union_lens%3Drecoveryid%253A201_11.20.207.176_1974284_1603940990104%253Bprepvid%253A201_11.20.207.176_1974284_1603940990104"}'

        # url编码 --> quote()     url解码 --> unquote()
        data = quote(str_data, 'utf-8')

        tme = str(time.time()).replace('.', '')[0:13]

        sgn = self.sign(self.token, tme, self.appKey, str_data)

        url = f'https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/?jsv=2.5.1&appKey={appKey}&t={tme}&sign={sgn}&api=mtop.alimama.union.xt.en.api.entry&v=1.0&AntiCreep=true&timeout=20000&AntiFlood=true&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data={data}'

        headers = {'cookie': self.cookie}  # 未使用proxies
        try:
            with requests.get(url, headers=headers) as res:
                html = res.text
                res_str = html.split('"resultList":')[-1].split('}},"ret":')[0]
                res_list = json.loads(res_str)
                if self.switch_save == 0:
                    self.switch_save_0(res_list)
                elif self.switch_save == 1:
                    self.switch_save_1(res_list)
                elif self.switch_save == 2:
                    self.switch_save_2(res_list)
                else:
                    print('存储部分设置有误!')
        except Exception as e:
            print('second_requests 出错: ', e)

    # 保存进csv
    def switch_save_0(self, res_list):
        from save_csv import save_csv
        csv_file_name = self.file_name + '.csv'
        # 返回该页面所有的 itemId 存入 L_itemId 列表中
        # print(res_list)
        self.L_itemId += save_csv(res_list, csv_file_name)
        print('\n已完成爬取项目数目: ', len(self.L_itemId))

    # 保存进mysql数据库
    def switch_save_1(self, res_list):
        from save_mysql import save_mysql
        self.L_itemId += save_mysql(res_list, self.str_searchContent)
        print('\n已完成爬取项目数目: ', len(self.L_itemId))

    # 保存进mongodb数据库
    def switch_save_2(self, res_list):
        from save_mongoDB import save_mongoDB
        self.L_itemId += save_mongoDB(res_list, self.str_searchContent)
        print('\n已完成爬取项目数目: ', len(self.L_itemId))

    # 关键字搜索爬虫，调用第一/第二次请求
    def get_search_page(self):
        print('搜索页面 线程启动: ', threading.current_thread().name)
        for i in range(1, self.num_page + 1):
            self.first_requests()  # 放在遍历外，可以调整获取cookie的频率
            self.second_requests()
            print('完成第 {} 页爬取\n====================\n'.format(i))

    # 根据itemId来爬取该评论
    def get_comments_page(self):
        print('评论页面 线程启动: ', threading.current_thread().name)
        time.sleep(5)
        n = 3  # 三次请求 self.L_itemId 无返回, 则认为所有数据爬取完毕
        while n > 0:
            itemId = self.L_itemId.pop(0)
            try:
                print(f'{threading.current_thread().name}开始爬取评论')
                self.get_comments(itemId)
                n = 3
            except Exception as e:
                print(f'{itemId}评论爬取错误：', e)
                n -= 1
                time.sleep(5)

    # 请求评论的数据
    def get_comments(self, itemId):
        itemId, sellerId, isTmall = itemId  # itemId是一个元组（itemId，isTmall）
        # 判断是否天猫
        if isTmall == 'true':
            url = f'https://rate.tmall.com/list_detail_rate.htm?itemId={itemId}&sellerId={sellerId}'
            referer = f'https://detail.tmall.com/item.htm?id={itemId}'
        else:
            url = f'https://rate.taobao.com/feedRateList.htm?auctionNumId={itemId}&currentPageNum=1&pageSize={self.num_pageSize}'
            referer = f'https://item.taobao.com/item.htm?id={itemId}'
        # x5sec=7b22726174656d616e616765723b32223a223963366265636632636238303536383262633632636134386461353832366363434c666a6e763046454c6643785962457366444e6777453d227d;
        headers = {
            'cookie': 'x5sec=7b22726174656d616e616765723b32223a223963366265636632636238303536383262633632636134386461353832366363434c666a6e763046454c6643785962457366444e6777453d227d;',
            'referer': referer,
        }
        proxies = self.proxies
        with requests.get(url, headers=headers) as res:
            # 判断是否天猫
            if isTmall == 'true':
                comments = res.text.split('"rateList":')[1].split(',"searchinfo"')[0]
            else:
                comments = res.text.split('"comments":')[1].split(',"currentPageNum"')[0]
            comments_list = json.loads(comments)
            # 保存数据
            self.save_comments(comments_list, itemId)

    # 保存评论的数据入mongoDB
    def save_comments(self, comments_list, itemId):
        from save_comment_mongDB import save_mongoDB
        save_mongoDB(comments_list, itemId)
        print(f'\n{itemId}--> mongoDB入库成功'+'='*30)

    def run(self):
        tme = str(time.time()).replace('.', '')[0:13]
        self.file_name = '搜索页面' + '_' + self.str_searchContent + '_' + str(self.num_pageSize) + '_' + str(
            self.num_page) + '_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(tme[:10]))).replace(' ',
                                                                                                             '_').replace(
            ':', '_')

        threads = []
        # 一条线程爬取搜索页面
        if self.threads_num_get_pages != 1:
            print('建议设置 threads_num_get_pages = 1')
        for t in range(threads_num_get_pages):
            thread0 = threading.Thread(target=self.get_search_page, args=())
            threads.append(thread0)

        # 新建线程爬取详情页面
        if self.threads_num_get_comments:
            for i in range(self.threads_num_get_comments):
                thread = threading.Thread(target=self.get_comments_page, args=())
                threads.append(thread)

        # 启动多线程
        for t in threads:
            t.start()

        for t in threads:
            t.join()
            print('关闭线程: ', t.name)

        print('主线程结束！', threading.current_thread().name)


if __name__ == "__main__":
    # 搜索配置
    # 搜索内容
    str_searchContent = '连衣裙'
    # 每页显示数量
    num_pageSize = 100
    # 淘宝评论爬取数量，（天猫理论上默认是所有评论）
    taobao_comments_num = 100
    # 从第一页 至 第几页（理论上可穷尽阿里服务器），推荐填入 1~100 ，页数再大则显示的内容匹配度不足
    num_page = 2
    # 阿里服务编号，12574478 固定不要更改，如菜鸟裹裹为 12574478 固定
    appKey = '12574478'
    # 储存--------------------------------------------
    # switch_save = 0  # 本地 csv 存储
    switch_save = 1  # mysql 存储
    # switch_save = 2 # mongoDB 存储

    # 开启线程的数量
    threads_num_get_pages = 1  # 抓取搜索页的线程数, 默认为 1, 建议也为1
    threads_num_get_comments = 2  # 抓取评论页的线程数,当为 0 时,不抓取详情页面(评论)； -->待开发完善

    # 代理的设置
    proxies = {
        'http': 'http://103.233.152.140:80',
        # "https": '',
    }

    TaoBao(str_searchContent, num_pageSize, num_page, appKey,
           threads_num_get_pages, switch_save, proxies, threads_num_get_comments, taobao_comments_num)
