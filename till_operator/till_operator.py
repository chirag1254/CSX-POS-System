from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang.builder import Builder
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import re
from pymongo import MongoClient

Window.size = (1500, 1500)



Builder.load_file('till_operator/Operator.kv')


class OperatorWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = []
        self.qty = []
        self.total = 0.00
        self.client = MongoClient()
        self.db = self.client.silverpos2
        self.products =self.db.stocks
        

        
    def logout(self):
        self.parent.parent.current = 'scrn_si'
    def update_purchase(self):
        

        pcode = self.ids.code_inp.text

        products_container = self.ids.product_container
        
        
        
        product = self.products.find_one({"product_code" :pcode})
        print(product)
        
        if pcode == None  :
            pass
        else:
            details = MDBoxLayout(
                size_hint_y=None, height=30, pos_hint={"top": 1})
            products_container.add_widget(details)
            code = MDLabel(text=pcode, size_hint_x=0.1)
            name = MDLabel(text= product['product_name'], size_hint_x=0.2)
            qty = MDLabel(text="1", size_hint_x=0.1)
            disc = MDLabel(text="0.00", size_hint_x=0.2)
            price = MDLabel(text="0.00", size_hint_x=0.1)
            total = MDLabel(text="0.00", size_hint_x=0.2)

            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

            pqty = str(1)
            pname = "Product One"

            
            self.ids.cur_item.text = pname

            pprice = float(price.text)
            self.total += pprice
            self.ids.cur_price.text = str(pprice)
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t' + str(self.total)

            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]

            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i

            if ptarget >= 0:
                pqty = self.qty[ptarget] + 1
                self.qty[ptarget] = pqty
                expr = '%s\t\tx\d\t' % (pname)
                rexpr = pname + '\t\tx'+str(pqty)+'\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total

            else:
                self.cart.append(pcode)
                self.qty.append(1)

                nu_preview = '\n\n'.join(
                    [prev_text, pname+'\t\tx'+str(pqty)+'\t\t'+str(pprice), purchase_total])
                preview.text = nu_preview


class OperatorApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        

        return OperatorWindow()


if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()
