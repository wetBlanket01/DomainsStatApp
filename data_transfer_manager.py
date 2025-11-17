import time
from typing import Dict
import flet as ft
import pandas as pd


class DataTransferManager:
    def __init__(self, final_domains: Dict, dynamic: pd.DataFrame):
        print('=Data transfer manager - initialization=')

