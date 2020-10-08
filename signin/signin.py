from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.lang.builder import Builder
# from kivymd.uix.toolbar import MDToolbar
# from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from pymongo import MongoClient
import hashlib


Builder.load_file('signin/Signin.kv')


class SigninWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            

    def validate_user(self):
        

        client = MongoClient()
        db = client.silverpos2
        users = db.users

        usr = self.ids.user_field
        pwd = self.ids.pwd_field

        info = self.ids.info

        uname = usr.text
        passw = pwd.text
    
        usr.text = ''
        pwd.text = ''

        if uname == '' or passw == '':
            info.text = "username or password required"
            info.theme_text_color:"Custom"
            info.text_color  : (0,0,1,1)
            
        else:
            user = users.find_one({"user_name": uname})
            
            if user == None:
                info.text = "Invalid Username or password!!"
            else:
                
                if passw == user['password']:
                    des = user['designation']
                    info.text = ''
                    
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_ad'
                    else:
                        self.parent.parent.current = 'scrn_op'

                else:
                    info.text = "Invalid Username or password!!"


    

class SigninApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"

        return SigninWindow()


if __name__ == "__main__":
    sa = SigninApp()
    sa.run()
