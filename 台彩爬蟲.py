import pandas as pd
import numpy as np
import logging
import requests
from lxml import etree

# 訊息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s')

# 檢查輸入是否正確


def err(e, s, **all_type_name):
    while True:
        try:
            inp = input(s)
            if e == 'type game':
                if all_type_name[inp]:
                    return inp
                else:
                    raise Exception
            elif e == 'year':
                if inp in [str(i) for i in range(103, 110)]:
                    return inp
                else:
                    raise Exception
            elif e == 'month':
                if inp in [str(i) for i in range(1, 13)]:
                    return inp
                else:
                    raise Exception
        except Exception:
            print('-----輸入錯誤 請重新輸入-----', e)


# 選擇遊戲種類
# 送出get請求
class Color_scroll:
    def __init__(self):
        self.s = '威力彩/大樂透/今彩539/雙贏彩/3星彩/4星彩/38樂合彩/49樂合彩/39樂合彩 選擇遊戲種類? '
        self.y = '103~109 選擇年份？ '
        self.m = '1~12 選擇月份？ '

        self.all_type_name = {"威力彩": "SuperLotto638",
                              "大樂透": "Lotto649",
                              "今彩539": "Dailycash",
                              "雙贏彩": "Lotto1224",
                              "3星彩": "3D",
                              "4星彩": "4D",
                              "38樂合彩": "38m6",
                              "49樂合彩": "49m6",
                              "39樂合彩": "39m5"}

        self.my_type_name = err('type game', self.s, **self.all_type_name)
        self.year = err('year', self.y)
        self.month = err('month', self.m)

        self.url = f'https://www.taiwanlottery.com.tw/Lotto/{self.all_type_name[self.my_type_name]}/history.aspx'
        self.html_get = requests.get(self.url)
        self.xpath_html_get = etree.HTML(self.html_get.text)

        self.my_requests()

    # 送出post請求及formData-data
    def my_requests(self):
        self.drop_down_text = self.xpath_html_get.xpath(
            "//*/table/tr/td/select/option/text()")
        self.drop_down_value = self.xpath_html_get.xpath(
            '//*/table/tr/td/select/option/@value')
        self.drop_downList1_dict = dict(
            zip(self.drop_down_text, self.drop_down_value))

        self.formData = {'__EVENTTARGET': "",
                         '__EVENTARGUMENT': "",
                         '__LASTFOCUS': "",
                         '__VIEWSTATE': self.xpath_html_get.xpath('//*[@id="__VIEWSTATE"]//@value'),
                         '__VIEWSTATEGENERATOR': self.xpath_html_get.xpath('//*[@id="__VIEWSTATEGENERATOR"]//@value'),
                         '__VIEWSTATEENCRYPTED': "",
                         '__EVENTVALIDATION': self.xpath_html_get.xpath('//*[@id="__EVENTVALIDATION"]//@value'),
                         str(self.xpath_html_get.xpath('//*/table/tr/td/select/@name')): self.drop_downList1_dict[self.my_type_name],
                         str(self.xpath_html_get.xpath('//*/table/tr/td/ul/li[3]/input/@name')[0]): 'radYM',
                         str(self.xpath_html_get.xpath('//*/table/tr/td/ul/li[3]/select/@name')[0]): self.year,
                         str(self.xpath_html_get.xpath('//*/table/tr/td/ul/li[3]/select/@name')[1]): self.month,
                         str(self.xpath_html_get.xpath('//*/table/tr/td/ul/li[3]/input/@name')[1]): '查詢'}

        self.html_post = requests.post(self.url, data=self.formData)
        self.my_xpath = etree.HTML(self.html_post.text)

        print()
        print(f'{self.my_type_name}---{self.year}年---{self.month}月---開獎結果')
        print()

# numpy＆pandas表


def np_pd(period, number):
    period_len = len(period)
    total＿number = int(len(number) / period_len)
    number_array = np.array(number).reshape(period_len, total＿number)

    index_columns = list(range(1, total＿number+1))
    data_frame = pd.DataFrame(
        number_array, index=period, columns=index_columns)
    return data_frame

# 抓取期別＆號碼


class Number(Color_scroll):
    def __init__(self):
        super().__init__()

        # 檢查有無資料
        self.e = self.my_xpath.xpath(
            '//*[@id="right"]/table/tr/td/ul/li[3]/span//text()')
        if self.e != []:
            print('------------', ''.join(self.e), '-----------')
            if input("輸入 'e'退出/其他鍵重新執行") == 'e':
                return
            else:
                super().__init__()

        if self.my_type_name == '威力彩':
            self.power_lottery()

        elif self.my_type_name == '大樂透':
            self.big_lottery()

        elif self.my_type_name == '今彩539':
            self.Jincai_539()

        elif self.my_type_name == '雙贏彩':
            self.win_win()

        elif self.my_type_name == '3星彩':
            self.star_color_3()

        elif self.my_type_name == '4星彩':
            self.star_color_4()

        elif self.my_type_name in ['38樂合彩', '49樂合彩', '39樂合彩']:
            self.lottery_38_49_39()

    # 威力彩
    def power_lottery(self):
        self.period = self.my_xpath.xpath(
            '//*/tr/td/table/tr[2]/td[1]/span/text()')
        self.number = self.my_xpath.xpath(
            '//*//tr/td/table//tr[5]/td/span/text()')

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 大樂透
    def big_lottery(self):
        self.period = self.my_xpath.xpath(
            '//*/tr/td/table/tr[2]/td[1]/span/text()')
        self.number = self.my_xpath.xpath(
            '//*/tr/td/table/tr[4]/td/span//text()')

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 今彩539
    def Jincai_539(self):
        self.period = self.my_xpath.xpath(
            '//*/tr/td/table/tr[2]/td[1]/span/text()')
        self.number = []
        for i in self.my_xpath.xpath('//*/tr/td/table/tr[2]/td/span/text()'):
            if len(i) == 2:
                self.number.append(i)

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 雙贏彩
    def win_win(self):
        self.period = self.my_xpath.xpath(
            '//*/tr/td/table/tr[2]/td[1]/span/text()')
        self.number = self.my_xpath.xpath(
            '//*/tr/td/table/tr[4]/td/span/span/text()')

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 3星彩
    def star_color_3(self):
        self.period = self.my_xpath.xpath(
            '//*/table/tr/td/table/tr[3]/td[1]/text()')
        self.number = self.my_xpath.xpath(
            '//*/table/tr/td/table/tr[3]/td[3]/span/text()')

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 4星彩
    def star_color_4(self):
        self.period = self.my_xpath.xpath(
            '//*/table/tr/td/div[3]/table/tr[3]/td[1]/text()')
        self.number = self.my_xpath.xpath(
            '//*/table/tr/td/div[3]/table/tr[3]/td[3]/span/text()')

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)

    # 38樂合彩, 49樂合彩, 39樂合彩
    def lottery_38_49_39(self):
        self.period = self.my_xpath.xpath(
            '//*/tr/td/table/tr[2]/td[1]/span/text()')
        self.number = []
        for i in self.my_xpath.xpath('//*/tr/td/table/tr[2]/td/span/text()'):
            if len(i) == 2:
                self.number.append(i)

        self.data_frame = np_pd(self.period, self.number)
        print(self.data_frame)


if __name__ == "__main__":
    Number()
