from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from pymongo import MongoClient
from collections import OrderedDict
from kivy.core.window import Window


Window.size = (1700, 1500)


Builder.load_string("""
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: 'CustLabel'
    
        
        id : table_floor
        RecycleGridLayout:
            id : table_floor_cols
            
            spacing: 5
            default_size : (None,250)
            default_size_hint : (1,None)
            size_hint_y : None
            height : self.minimum_height
<CustLabel@Label>:
    bcolor:(1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos


""")


class DataTable(MDBoxLayout):
    def __init__(self, table='', **kwargs):
        super().__init__(**kwargs)

        products = table
        col_titles = [k for k in products.keys()]
        row_len = len(products[col_titles[0]])
        self.coloumns = len(col_titles)

        table_data = []

        for t in col_titles:
            table_data.append(
                {'text': str(t).capitalize(), 'size_hint_y': None, 'height': 40, 'color': [1, 1, 1, 1],
                 'halign': 'center', 'bcolor': (0.06, 0.45, 0.45, 1)})

        for r in range(row_len):
            for t in col_titles:
                table_data.append({'text': str(products[t][r]), 'size_hint_y': None,
                                   'height': 30, 'color': [0, 0, 0, 1], 'halign': 'center', 'bcolor': (1, 1, 1, 1)})
        self.ids.table_floor.data = table_data
        self.ids.table_floor_cols.cols = self.coloumns


# class DataTableApp(MDApp):
#     def build(self):
#         self.theme_cls.primary_palette = 'Blue'
#         return DataTable()


# if __name__ == "__main__":
#     DA = DataTableApp()
#     DA.run()
