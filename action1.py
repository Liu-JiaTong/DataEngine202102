import requests
from bs4 import BeautifulSoup
import pandas as pd


# 网页HTML信息获取函数
# 输入参数：url: 获取信息的url链接
#         headers: 请求头
# 返回值：  BeautifulSoup
def creat_bs(url, headers,):
    # 通过get方法获取网页相应的信息
    response = requests.get(url, headers=headers, timeout=10)
    # 从获取到的response信息中提取出html代码
    html_text = response.text
    # 通过html_text创建BeautifulSoup对象
    bs = BeautifulSoup(html_text, 'html.parser')
    return bs


# 汽车投诉信息获取函数
# 输入参数：url: 获取信息的url链接
#         headers: 请求头
def car_complain_spider(url, headers, data_save_file='csv_out.csv'):
    csv_header = []
    # 用于存取每页获取到的数据
    csv_data = []
    # 临时存储表格单行信息
    table_row_data = []
    # 读取当前页的信息
    bs = creat_bs(url, headers)
    # 获取总的页数
    page_num = int(bs.find_all(name='a', text='尾页')[0]['href'].split('-')[-1].split('.')[0])
    # 遍历每一页
    # 起始页码
    page_pre = 1
    for page in range(1, page_num + 1):
        # 刷新下一页的url地址
        url_search = url.replace('-' + str(page_pre) + '.', '-' + str(page) + '.')
        # 读取当前页的信息
        bs = creat_bs(url_search, headers)
        # 保存当前访问页码便于更新下一次访问url
        page_pre = page
        # 通过class名称找到投诉信息表格
        table_all = bs.find_all(name='table', attrs={"class": "ar_c ar_c1"})
        # 读取表格的每一行信息
        table_info = table_all[0].contents
        # 只有第一页需要读取表头（th）, 其他页不读
        if page > 1:
            table_info.pop(0)
        # 解析每一行信息
        for th_td in table_info:
            # 解析每一行的每一列的信息
            for data in th_td:
                # 缓存一行的信息
                table_row_data.append(data.text)
            # 存储一行的信息
            csv_data.append(table_row_data.copy())
            # 清空一行的缓存信息
            table_row_data.clear()
        # 创建Pandas DataFrame
        data_out = pd.DataFrame(csv_data)
        # 保存信息到csv(第一页数据将所有原始覆盖，后面追加)
        if page > 1 :
            data_out.to_csv(data_save_file, mode='a', index=False, header=False, encoding='utf_8_sig')
        else:
            data_out.to_csv(data_save_file, mode='w', index=False, header=False, encoding='utf_8_sig')
        # 当前页的临时数据清空
        csv_data.clear()
        print("搜索第" + str(page) + "页完成")
    print("全部搜索完成")


if __name__ == '__main__':
    # 获取信息的url链接
    url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
    # 请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    # 获取到的数据保存地址
    data_save_file = 'car_complain.csv'
    car_complain_spider(url, headers, data_save_file)
