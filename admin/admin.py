from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.floatlayout import FloatLayout
from kivy.lang .builder import Builder
from kivymd.uix.label import MDLabel
from pymongo import MongoClient
from collections import OrderedDict
from utils.data_tables import DataTable
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivymd.uix.button import MDFlatButton
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg as FCK
from kivy.core.window import Window



Builder.load_file('admin/Admin.kv')

class Tab(FloatLayout, MDTabsBase):
    pass


class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.4, .4)


class AdminWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notify = Notify()

        users = self.get_users()
        print(users)
        client = MongoClient()
        db = client.silverpos2
        self.users = db.users
        self.products = db.stocks

        # user_tab
        content = self.ids.user_box
        users = self.get_users()
        usertable = DataTable(table=users)
        content.add_widget(usertable)

        # product_tab
        content_1 = self.ids.products_box
        products = self.get_products()
        usertable_1 = DataTable(table=products)
        content_1.add_widget(usertable_1)

        # Adding Products tp Analysis Spinner

        product_codes = []
        product_names = []
        spinvals = []
        for product in self.products.find():
            product_codes.append(product['product_code'])
            product_names.append(product['product_name'])
        for x in range(len(product_codes)):
            line = " | ".join([product_codes[x], product_names[x]])
            spinvals.append(line)

        self.ids.target_product.values = spinvals
    
    

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_des = Spinner(text='Operator', values=[
                           'Operator', 'Administrator'])
        crud_subimt = MDFlatButton(text="Add", on_release=lambda x: self.add_user(
            crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_subimt)

    def add_user(self, first, last, user, pwd, des):
        content = self.ids.user_box
        content.clear_widgets()
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(
                MDLabel(text='All Fields Required!!',halign = 'center', bold = True ,theme_text_color="Error",markup = True))
            self.notify.open()
            
        else:
            self.users.insert_one({'first_name': first, 'last_name': last,
                                   'user_name': user, 'password': pwd, 'designation': des, 'date': datetime.now()})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    

    def remove_user_field(self):
        target = self.ids.ops_fields
        target.clear_widgets()

        crud_user = TextInput(hint_text='User Name', size_hint_x=0.8)
        crud_remove = MDFlatButton(
            text="Remove", on_release=lambda x: self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_remove)

    def remove_user(self, user1):
        content = self.ids.user_box

        content.clear_widgets()
        if user1 == '' :
            self.notify.add_widget(
                MDLabel(text='All Fields Required!!',halign = 'center', bold = True ,theme_text_color="Error",markup = True))
            self.notify.open()
        else:     
            self.users.remove({'user_name': user1})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name', focus=True)
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_des = Spinner(text='Operator', values=[
                           'Operator', 'Administrator'])
        crud_subimt = MDFlatButton(text="Update", on_release=lambda x: self.update_user(
            crud_first.text, crud_last.text,
            crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_subimt)

    def update_user(self, first, last, user, pwd, des):
        content = self.ids.user_box
        content.clear_widgets()
        if first == '' or last == '' or user == '' or pwd == ''  :
            self.notify.add_widget(
                MDLabel(text='All Fields Required!!',halign = 'center', bold = True ,theme_text_color="Error",markup = True))
            self.notify.open()
        else:
            self.users.update_one({'user_name': user}, {'$set': {'first_name': first, 'last_name': last,
                                                             'user_name': user, 'password': pwd, 'designation': des, 'date': datetime.now()}})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_wieght = TextInput(hint_text='Product Weight')
        crud_in_stock = TextInput(hint_text='Product In_stock')
        crud_sold = TextInput(hint_text='Sold')
        crud_order = TextInput(hint_text='Order')
        crud_last_purchase = TextInput(hint_text='Last_purchase')
        crud_subimt_p = MDFlatButton(text="Add", on_release=lambda x: self.add_product(
            crud_code.text, crud_name.text, crud_wieght.text, crud_in_stock.text, crud_sold.text, crud_order.text, crud_last_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_wieght)
        target.add_widget(crud_in_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_subimt_p)

    def add_product(self, code, name, weight, in_stock, sold, order, last_purchase):
        content_1 = self.ids.products_box
        content_1.clear_widgets()

        if  code == '' or name == '' or weight == '' or in_stock == '' or order == '' or last_purchase == ''  :
            self.notify.add_widget(
                MDLabel(text='All Fields Required!!',halign = 'center', bold = True ,theme_text_color="Error",markup = True))
            self.notify.open()
        else:
            self.products.insert_one({'product_code': code, 'product_name': name,
                                    'product_weight': weight, 'in_stock': in_stock, 'sold': sold,
                                    'order': order, 'last_purchase': last_purchase})

        products = self.get_products()
        p_table = DataTable(table=products)
        content_1.add_widget(p_table)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code', focus=True)
        crud_name = TextInput(hint_text='Product Name')
        crud_wieght = TextInput(hint_text='Product Weight')
        crud_in_stock = TextInput(hint_text='Product In_stock')
        crud_sold = TextInput(hint_text='Sold')
        crud_order = TextInput(hint_text='Order')
        crud_last_purchase = TextInput(hint_text='Last_purchase')
        crud_subimt_p = MDFlatButton(text="Update", on_release=lambda x: self.update_product(
            crud_code.text, crud_name.text, crud_wieght.text, crud_in_stock.text, crud_sold.text, crud_order.text, crud_last_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_wieght)
        target.add_widget(crud_in_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_order)
        target.add_widget(crud_last_purchase)
        target.add_widget(crud_subimt_p)

    def update_product(self, code, name, weight, in_stock, sold, order, last_purchase):
        content_1 = self.ids.products_box
        content_1.clear_widgets()
        self.products.update_one({'product_code': code}, {"$set": {'product_code': code, 'product_name': name,
                                                                   'product_weight': weight, 'in_stock': in_stock, 'sold': sold,
                                                                   'order': order, 'last_purchase': last_purchase}})

        products = self.get_products()
        p_table = DataTable(table=products)
        content_1.add_widget(p_table)

    def remove_product_field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code')
        crud_subimt_p = MDFlatButton(
            text="Remove", on_release=lambda x: self.remove_product(crud_code.text))
        target.add_widget(crud_code)
        target.add_widget(crud_subimt_p)

    def remove_product(self, code):
        content_1 = self.ids.products_box
        content_1.clear_widgets()

        self.products.remove({'product_code': code})

        products = self.get_products()
        p_table = DataTable(table=products)
        content_1.add_widget(p_table)

    def get_users(self):

        client = MongoClient()
        db = client.silverpos2
        users = db.users
        _users = OrderedDict(
            first_name={},
            last_name={},
            user_name={},
            password={},
            designation={}
        )

        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():

            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 10:
                pwd = pwd[:13] + "...."
            passwords.append(pwd)
            designations.append(user['designation'])
        # print(last_name)
        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['first_name'][idx] = first_names[idx]
            _users['last_name'][idx] = last_names[idx]
            _users['user_name'][idx] = user_names[idx]
            _users['password'][idx] = passwords[idx]
            _users['designation'][idx] = designations[idx]
            idx += 1

        return _users

    def get_products(self):
        client = MongoClient()
        db = client.silverpos2
        products = db.stocks
        _stocks = OrderedDict()

        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['order'] = {}
        _stocks['last_purchase'] = {}

        product_codes = []
        product_names = []
        product_weights = []
        in_stocks = []
        solds = []
        orders = []
        last_purchases = []

        for product in products.find():
            product_codes.append(product['product_code'])
            product_names.append(product['product_name'])
            product_weights.append(product['product_weight'])
            in_stocks.append(product['in_stock'])
            solds.append(product['sold'])
            orders.append(product['order'])
            last_purchases.append(product['last_purchase'])
        # print(product_name)
        products_length = len(product_codes)
        idx = 0
        while idx < products_length:
            _stocks['product_code'][idx] = product_codes[idx]
            _stocks['product_name'][idx] = product_names[idx]
            _stocks['product_weight'][idx] = product_weights[idx]
            _stocks['in_stock'][idx] = in_stocks[idx]
            _stocks['sold'][idx] = solds[idx]
            _stocks['order'][idx] = orders[idx]
            _stocks['last_purchase'][idx] = last_purchases[idx]
            idx += 1

        return _stocks

    def view_stats(self):
        plt.cla()
        self.ids.analysis_res.clear_widgets()
        target_product = self.ids.target_product.text
        target = target_product[:target_product.find(' | ')]
        name = target_product[target_product.find(' | '):]

        df = pd.read_csv(
            '/home/techy/Documents/POS System/admin/products_purchase.csv')
        purchases = []
        dates = []
        count = 0
        for x in range(len(df)):
            if str(df.Product_Code[x]) == target:
                purchases.append(df.Purchased[x])
                dates.append(count)
                count += 1
        plt.bar(dates, purchases, color='teal', label=name)
        plt.ylabel('Total Purchases')
        plt.xlabel('day')
        self.ids.analysis_res.add_widget(FCK(plt.gcf()))
    def logout(self):
        self.parent.parent.current = 'scrn_si' 

class AdminApp(MDApp):
    def build(self):
        

        return AdminWindow()


if __name__ == "__main__":
    aa = AdminApp()
    aa.run()
