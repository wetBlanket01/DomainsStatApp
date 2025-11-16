import flet as ft
import pandas as pd
import os
import numpy as np


class ExcelDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        
        self.table_data = None

        if not os.path.exists(file_path):
            web_file_path = f'tables/{file_path}'
            if not os.path.exists(web_file_path):
                raise FileNotFoundError(f"File {file_path} does not exists")
            self.file_path = web_file_path
        else:
            self.file_path = file_path

    def process_table(self):
        self.df = pd.read_excel(self.file_path, index_col=None).reset_index(drop=True)

        self.table_name = 'final_domains' if 'state' in self.df.columns else 'Динамика сбора'

        if self.table_name == 'final_domains':
            self.table_data = self.df.set_index('domain')['state'].to_dict()

        else:
            self.table_data = self.df.insert(2, 'state', np.nan)
    
