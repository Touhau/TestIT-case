import json
import requests

from data import TestSection
from pars import Pars
from testit import dci_project


session = requests.Session()
session.auth = ()

class Tree:
    def get_child(self, node):
        print(node)
        child_mas_json = session.get(f'https://docs.ispsystem.com/rest/api/content/{node}/child?expand=page&limit=100').json()
        children = [i['id'] for i in child_mas_json['page']['results']]
        title_name = session.get(f'https://docs.ispsystem.com/rest/api/content/{node}').json()
        result = TestSection(title_name['title'])
        if not children:
            temp = Pars(node, session)
            result.children+=temp.get_info_from_table()
        else:
            for child in children:
                result.children.append(self.get_child(child))
        return result


a = Tree()
d = a.get_child(32017753)

with open('spec_error.txt', 'w'):
    pass

def print_log(id_):
    ADDR = ""
    KEY = ""
    headers = {"Authorization": f"PrivateToken {KEY}"}
    headers["accept"] = "application/json"
    result_from = requests.get(f"{ADDR}/api/v2/sections/{id_}", headers=headers).json()
    try:
        return result_from['name']
    except:
        pass

def test_it_create(section, id_):
    print(print_log(id_))
    if type(section) == list:
        for element in section:
            test_it_create(section, id_)
    else:
        try:
            sect_id = dci_project.create_section(section.name, id_)['id']
        except Exception:
            write_error(section.name)
            return
        for child in section.children:
            if type(child) == list:
                for element in child:
                    create_case(element, sect_id)
            else:
                create_case(child, sect_id)
            

def create_case(child, s_id):
    if isinstance(child, TestSection):
        test_it_create(child, s_id)
    else:
        return dci_project.create_test_case(s_id, child.name, child.is_positive)

def write_error(id_):
    with open('spec_error.txt', 'a') as se:
        se.write(f'Что то на {id_} \n')
    return

print("Начали запись")
test_it_create(d, None)


# 32017753
# by Touhau