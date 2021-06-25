import re
import json

from data import TestSection, TestCase

import requests
from bs4 import BeautifulSoup

class Pars:
    def __init__(self, id, session):
        self.session = session
        self.id = id
        page = self.session.get(f'https://docs.ispsystem.com/plugins/viewstorage/viewpagestorage.action?pageId={self.id}').text
        self.soup = BeautifulSoup(page, 'lxml')
        self.find_h2 = self.soup.find_all('h2')
        if self.find_h2[1:]:
            if self.find_h2[1].text == "Легенда":
                self.find_h2 = self.find_h2[2:]
            else:
                self.find_h2 = self.find_h2[1:]
        self.find_h3 = self.soup.find_all('h3')

    # Убираем все лишнее из строки 
    def get_mas_without_empty(self, mas):
        new_mas = []
        for i in mas:
            if i != '':
                new_mas.append(re.match(r"^[HMLBEF|.]*(.*)", i).group(1).strip().rstrip('.').lstrip('-'))
        return new_mas

    def get_str_without(self, st):
        st = st.replace("\n",'')
        temp = re.match(r"^[\d. ]*(.*)", st.strip())
        return temp.group(1)

    # Делим на позитивные и негативные строки
    def get_pozneg_dict(self, mas):
        negpoz_dict = {}
        light = True
        temp_poz = []
        temp_neg = []
        for i in mas:
            if i != 'Positive:' and i != 'Negative:' and light == True:
                temp_poz.append(i)      
            elif i == 'Negative:':
                light = False
            elif i != 'Positive:' and i != 'Negative:' and light == False:
                temp_neg.append(i)
        negpoz_dict.update({'Positive': temp_poz})
        if light == False:
            negpoz_dict.update({'Negative': temp_neg})
        return negpoz_dict


    def parse_case(self, text):
        list_test_case = []
        temp = self.get_mas_without_empty(text.split('\n'))
        poz_neg_dict = self.get_pozneg_dict(temp)
        for key, cases in poz_neg_dict.items():
            for case in cases:
                list_test_case.append(TestCase(case, key == "Positive"))
        return list_test_case

    def get_info_from_table(self):
        # Вытащили таблицы
        find_table = self.soup.find_all('table')
        equal_h2_table = 0
        table_section = []
        for table in find_table:
            if len(self.find_h3) == 0 and len(find_table) == len(self.find_h2):
                table_sect = TestSection(self.find_h2[equal_h2_table].text)
            else:
                table_sect = TestSection(str(equal_h2_table))
                self.error_log(self.id)
            find_tr = table.find_all('tr')[1:]
            for tr in find_tr:
                find_td = tr.find_all('td')[:2]       
                temp = self.get_str_without(find_td[0].text)
                child_section = TestSection(temp)
                child_section.children += self.parse_case(find_td[1].text)
                table_sect.children.append(child_section)
            table_section.append(table_sect)
            equal_h2_table+=1
        return table_section
    

    def error_log(self, id):
        with open('problem.txt','a') as log_file:
            title = self.session.get(f'https://docs.ispsystem.com/rest/api/content/{id}').json()["title"]
            log_file.write(f'В секции: {title} проблемы\n')
        


if __name__ == "__main__":
    
    a = Pars(45648614)
    w = a.get_info_from_table()



# by Touhau