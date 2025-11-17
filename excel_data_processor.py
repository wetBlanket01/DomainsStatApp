import pandas as pd
import os
from pathlib import Path
from typing import Dict, Optional, Union
import logging
import time
import numpy as np

logger = logging.getLogger(__name__)


class ExcelDataProcessor:
    """Обработчик Excel файлов для таблиц final_domains и динамики сбора"""

    FINAL_DOMAINS = "final_domains"
    DYNAMICS = "dynamics_collection"

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        self.table_name: Optional[str] = None
        self.table_data: Union[pd.DataFrame, Dict, None] = None

        self._validate_file()

    def _validate_file(self) -> None:
        """Валидация файла"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл {self.file_path} не существует")

        if self.file_path.suffix.lower() not in ['.xlsx', '.xls']:
            raise ValueError(f"Файл {self.file_path} не поддерживается")

    def _detect_table_type(self) -> str:
        """Определение типа таблицы"""
        columns_set = set(self.df.columns.str.lower())

        if {'domain', 'state'}.issubset(columns_set):
            return self.FINAL_DOMAINS
        elif {'домен', 'страна'}.issubset(columns_set):
            return self.DYNAMICS
        else:
            raise ValueError("Неизвестный формат таблицы")

    def _process_final_domains(self) -> Dict:
        """Обработка таблицы final_domains"""
        logger.info("Обработка таблицы final_domains")

        # Валидация обязательных колонок
        required_columns = ['domain', 'state']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing_columns}")

        return self.df.set_index('domain')['state'].to_dict()

    def _process_dynamics(self) -> pd.DataFrame:
        """Обработка таблицы динамики сбора."""
        logger.info("Обработка таблицы динамики сбора")

        # Добавляем колонку state если её нет
        if 'state' not in self.df.columns:
            self.df.insert(2, 'state', np.nan)
            logger.debug("Добавлена колонка 'state'")

        return self.df

    def process_table(self) -> Union[pd.DataFrame, Dict]:
        try:
            logger.info(f"Начало обработки: {self.file_path}")

            self.df = pd.read_excel(self.file_path, index_col=None).reset_index(drop=True)
            self.table_name = self._detect_table_type()

            if self.table_name == self.FINAL_DOMAINS:
                self.table_data = self._process_final_domains()
            else:
                self.table_data = self._process_dynamics()

            logger.info(f"Успешно обработано {len(self.table_data)} записей")
            return self.table_data

        except Exception as e:
            logger.error(f"Ошибка при обработке файла {self.file_path}: {e}")
            raise

