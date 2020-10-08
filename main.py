from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.lang.builder import Builder
from signin.signin import SigninWindow
from admin.admin import AdminWindow
from till_operator.till_operator import OperatorWindow


Builder.load_file('Main.kv')


class MainWindow(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signin_widget = SigninWindow()
        self.admin_widget = AdminWindow()
        self.operator_widget = OperatorWindow()

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)
        self.ids.scrn_ad.add_widget(self.admin_widget)


class MainApp(MDApp):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    ma = MainApp()
    ma.run()