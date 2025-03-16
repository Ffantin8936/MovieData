import csv
import requests
from lxml import etree
import time

# 请求头
Headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': 'https://www.ygdy8.net/html/gndy/dyzz/index.html'
}
# 视频详情页Url拼接地址
Base_Url = 'https://www.ygdy8.net'

def Get_Detail(Details_Url):
    Detail_Url = Base_Url + Details_Url
    One_Detail = requests.get(url=Detail_Url, headers=Headers)
    One_Detail_Html = One_Detail.content.decode('gbk')
    Detail_Html = etree.HTML(One_Detail_Html)
    Detail_Content = Detail_Html.xpath("//div[@id='Zoom']//text()")
    Video_Name_CN,Video_Name,Video_Address,Video_Type,Video_language,Video_Date,Video_Number,Video_Time,Video_Daoyan,Video_Yanyuan_list = None,None,None,None,None,None,None,None,None,None
    for index, info in enumerate(Detail_Content):
        if info.startswith('◎译　　名'):
            Video_Name_CN = info.replace('◎译　　名', '').strip()
        if info.startswith('◎片　　名'):
            Video_Name = info.replace('◎片　　名', '').strip()
        if info.startswith('◎产　　地'):
            Video_Address = info.replace('◎产　　地', '').strip()
        if info.startswith('◎类　　别'):
            Video_Type = info.replace('◎类　　别', '').strip()
        if info.startswith('◎语　　言'):
            Video_language = info.replace('◎语　　言', '').strip()
        if info.startswith('◎上映日期'):
            Video_Date = info.replace('◎上映日期', '').strip()
        if info.startswith('◎豆瓣评分'):
            Video_Number = info.replace('◎豆瓣评分', '').strip()
        if info.startswith('◎片　　长'):
            Video_Time = info.replace('◎片　　长', '').strip()
        if info.startswith('◎导　　演'):
            Video_Daoyan = info.replace('◎导　　演', '').strip()
        if info.startswith('◎主　　演'):
            Video_Yanyuan_list = []
            Video_Yanyuan = info.replace('◎主　　演', '').strip()
            Video_Yanyuan_list.append(Video_Yanyuan)
            for x in range(index + 1, len(Detail_Content)):
                actor = Detail_Content[x].strip()
                if actor.startswith("◎"):
                    break
                Video_Yanyuan_list.append(actor)
    print(Video_Name_CN,Video_Date,Video_Time)
    f.flush()
    try:
        csvwriter.writerow((Video_Name_CN,Video_Name,Video_Address,Video_Type,Video_language,Video_Date,Video_Number,Video_Time,Video_Daoyan,Video_Yanyuan_list))
    except:
        pass


def spider(pages):
    for Page in range(1, pages + 1):
        Page_Url = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'.format(Page)
        Requ = requests.get(url=Page_Url, headers=Headers)
        Text = Requ.text
        Html = etree.HTML(Text)
        One_Page = Html.xpath('//*[@class="co_content8"]//a/@href')
        for i in One_Page:
            if i.startswith('/'):
                    try:
                        Get_Detail(i)
                    except:
                        pass
        print(f'==============第{Page}页爬取完毕！=================')


if __name__ == '__main__':
    with open('movies.csv','a',encoding='utf-8',newline='')as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(('Video_Name_CN','Video_Name','Video_Address','Video_Type','Video_language','Video_Date','Video_Number','Video_Time','Video_Daoyan','Video_Yanyuan_list'))
        spider(117)