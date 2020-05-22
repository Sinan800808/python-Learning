import tkinter as tk
from tkinter import ttk
import requests
import bs4
import re
import tkinter.messagebox
import datetime

# 爬取台鐵火車時刻表
class Requests():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}
        self.url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime'
        self.get_html = requests.get(self.url, headers=self.headers)
        self.get_Soup = bs4.BeautifulSoup(self.get_html.text, 'lxml')

        self.get_request()

    def get_request(self):
        self.starting_place = self.get_Soup.find_all('div', id=re.compile(r'\d{5}'))

        self.site_number_list = []
        for i in range(len(self.starting_place)):
            self.site_number_list.append([j.get('title') for j in self.starting_place[i].find_all('button')])

        self.city＿name_list = ['新北市', '台中市', '高雄市', '台北市', '嘉義市', '南投縣', '彰化縣', '新竹市',
                               '雲林縣', '嘉義縣', '宜蘭縣', '屏東縣', '花蓮縣', '新竹縣', '台東縣', '台南市', '桃園市', '基隆市', '苗栗縣']
        self.site_name_dict = {'新北市': self.site_number_list[0],
                               '台中市': self.site_number_list[1],
                               '高雄市': self.site_number_list[2],
                               '台北市': self.site_number_list[3],
                               '嘉義市': self.site_number_list[4],
                               '南投縣': self.site_number_list[5],
                               '彰化縣': self.site_number_list[6],
                               '新竹市': self.site_number_list[7],
                               '雲林縣': self.site_number_list[8],
                               '嘉義縣': self.site_number_list[9],
                               '宜蘭縣': self.site_number_list[10],
                               '屏東縣': self.site_number_list[11],
                               '花蓮縣': self.site_number_list[12],
                               '新竹縣': self.site_number_list[13],
                               '台東縣': self.site_number_list[14],
                               '台南市': self.site_number_list[15],
                               '桃園市': self.site_number_list[16],
                               '基隆市': self.site_number_list[17],
                               '苗栗縣': self.site_number_list[18]
                               }
        self.requests_Time = self.get_Soup.find('select', id='startTime').text

    def post_requests(self, startStation, endStation, rideDate, startingTime, endTime, TTKform):
        try:
            if re.search(r'(\d{4})/(\d{2})/(\d{2})', rideDate) and '' not in [startStation, endStation, startingTime, endTime]:
                d = datetime.datetime.today()
                r = rideDate.split('/')
                if int(r[0]) < d.year or int(r[1]) < d.month or int(r[2]) < d.day:
                    raise Exception('請輸入有效的日期')
            else:
                raise Exception('請確認輸入正確') 
        except Exception as e:
            tkinter.messagebox.showwarning('警吿', e)
            return

        self.FormDate = {'_csrf': '777d17bf-9b3b-4f5c-bf26-28aa2b3e9aef',
                         'startStation': startStation,
                         'endStation': endStation,
                         'transfer': 'ONE',
                         'rideDate': rideDate,
                         'startOrEndTime': 'true',
                         'startTime': startingTime,
                         'endTime': endTime,
                         'trainTypeList': 'ALL',
                         'query': '查詢'
                         }

        self.post_html = requests.post('https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime', data=self.FormDate, headers=self.headers)
        self.post_Soup = bs4.BeautifulSoup(self.post_html.text, 'lxml')

        if self.post_Soup.find('p', 'icon-fa warning'):
            tkinter.messagebox.showinfo('訊息', self.post_Soup.find('p', 'icon-fa warning').text)#檢查有無資料
            return

        self.form = self.post_Soup.find_all('tr', 'trip-column')
        self.formList = []
        for i in range(len(self.form)):
            self.CarType = self.form[i].find('td').find('a', 'links').text
            self.formList.append([j.text for j in self.form[i].find_all('td') if '\n' not in j])
            self.formList[i].insert(0, self.CarType)

        TTKform(self.post_Soup, self.formList)


# tkinter視窗
class Operation_Window(Requests):
    def __init__(self, win):
        super().__init__()

        win.title('火車時刻查詢')
        win.geometry('750x780')

        self.frame = tk.Frame(win)
        self.frame.pack(side=tk.TOP)

        self.departure_Label = tk.Label(self.frame, text='出發:')
        self.departure_Label.grid(row=0, column=0, pady=7)
        self.departure_city = ttk.Combobox(
            self.frame, width=15, values=self.city＿name_list)
        self.departure_city.grid(row=0, column=1, pady=5)
        self.departure_station = ttk.Combobox(self.frame, width=10)
        self.departure_station.grid(row=0, column=3, pady=5)

        self.arrival_Lable = tk.Label(self.frame, text='抵達:')
        self.arrival_Lable.grid(row=1, column=0, pady=7)
        self.arrival_city = ttk.Combobox(
            self.frame, width=15, values=self.city＿name_list)
        self.arrival_city.grid(row=1, column=1, pady=5)
        self.arrival_station = ttk.Combobox(self.frame, width=10)
        self.arrival_station.grid(row=1, column=3, pady=5)

        self.Entry_Lable = tk.Label(self.frame, text='日期:yyyy/mm/dd')
        self.Entry_Lable.grid(row=2, column=0)
        self.Entry_Date = tk.Entry(self.frame, width=17)
        self.Entry_Date.grid(row=2, column=1, pady=20)

        self.Starting_Time_Lable = tk.Label(self.frame, text='開始時間:')
        self.Starting_Time_Lable.grid(row=2, column=2)
        self.Starting_Time = ttk.Combobox(
            self.frame, width=10, values=self.requests_Time)
        self.Starting_Time.grid(row=2, column=3, pady=20)

        self.End_Time_Lable = tk.Label(self.frame, text='結束時間:')
        self.End_Time_Lable.grid(row=2, column=4)
        self.End_Time = ttk.Combobox(
            self.frame, width=10, values=self.requests_Time)
        self.End_Time.grid(row=2, column=5, pady=20)

        self.Inquire_Button = tk.Button(self.frame, text='查詢', width=6, height=2)
        self.Inquire_Button.grid(row=0, column=5, pady=7)

        self.frame_content = tk.Frame(win)
        self.frame_content.pack()

        self.scrollbar = tk.Scrollbar(win)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns_name = ('車種車次','出發時間','抵達時間','行駛時間','經由','全票','孩童票')
        self.tree = ttk.Treeview(self.frame_content, columns=columns_name, show="headings", yscrollcommand=self.scrollbar.set, height=33)
        for column in range(len(columns_name)):
            self.tree.column(columns_name[column] , width=100, anchor='center')
            self.tree.heading(columns_name[column], text=columns_name[column])
            self.tree.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar.config(command=self.tree.xview)

    def bind_object(self):
        self.departure_city.bind("<<ComboboxSelected>>", lambda x: self.select_station(self.departure_city.get(), self.departure_station))
        self.arrival_city.bind("<<ComboboxSelected>>", lambda x: self.select_station(self.arrival_city.get(), self.arrival_station))
        self.Inquire_Button['command'] = lambda: self.post_requests(
            self.departure_station.get(), self.arrival_station.get(), self.Entry_Date.get(), self.Starting_Time.get(), self.End_Time.get(), self.TTKform)

    def select_station(self, city_name, comboboxs):
        comboboxs['value'] = self.site_name_dict[city_name]

    def TTKform(self, post_Soup, *formList):
        departure_arrivals = post_Soup.find_all('span', 'location')
        
        if self.tree.get_children():
            [self.tree.delete(Id) for Id in self.tree.get_children()]
         
        for index in range(len(formList[0])):
            formList[0][index][1] = formList[0][index][1] + f'({departure_arrivals[0].text})'
            formList[0][index][2] = formList[0][index][2] + f'({departure_arrivals[1].text})'
        
            self.tree.insert('', index, values=formList[0][index])

        

win = tk.Tk()

o = Operation_Window(win)
o.bind_object()


win.mainloop()
