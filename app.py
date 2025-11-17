import flet as ft
from typing import Optional

from colors import Colors
from excel_data_processor import ExcelDataProcessor
from excel_upload_field import ExcelUploadField
from data_transfer_manager import DataTransferManager
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DomainsTablesApp:
    def __init__(self, page):
        self.page = page

        self._set_up_page()
        self._set_up_ui()
        self._set_up_data_state()

    def _set_up_page(self):
        """Настройка страницы и темы"""
        self.page.title = 'DomainsTablesApp'

        self.page.fonts = {
            "HackNerdFont": "https://cdn.jsdelivr.net/gh/ryanoasis/nerd-fonts@master/patched-fonts/Hack/Regular/HackNerdFont-Regular.ttf",
            "FallbackFont": "Arial"
        }

        self.page.window.min_width = 900
        self.page.window.min_height = 500

        self.page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE, font_family="HackNerdFont")
        self.page.theme_mode = ft.ThemeMode.DARK

    def _set_up_ui(self):
        """Настройка пользовательского интерфейса"""
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)

        self.header_text = ft.Text(
            value='Загрузите таблицы: final_domains, Динамика сбора',
            size=22,
            no_wrap=False,
            expand=True
        )

        self.notification_container = ft.Container(visible=False)
        self.download_button = ft.ElevatedButton(
            text="Скачать Таблицу",
            disabled=True,
            visible=False
        )

        self.upload_field = ExcelUploadField(file_picker=self.file_picker,
                                             notification_container=self.notification_container,
                                             on_file_loaded=lambda p: self._on_file_loaded(1, p))
        self.upload_field2 = ExcelUploadField(file_picker=self.file_picker,
                                              notification_container=self.notification_container,
                                              on_file_loaded=lambda p: self._on_file_loaded(2, p))

    def _set_up_data_state(self):
        """Инициализация состояния данных"""
        self.file1_processor: Optional[ExcelDataProcessor] = None
        self.file2_processor: Optional[ExcelDataProcessor] = None
        self.transfer_manager: Optional[DataTransferManager] = None

    def _on_file_loaded(self, file_number: int, processor: ExcelDataProcessor):
        """Обработчик загрузки файла"""

        try:
            logger.info(f"Файл {file_number} загружен: {processor.table_name}")

            if file_number == 1:
                self.file1_processor = processor
            else:
                self.file2_processor = processor

            # self._update_progress()
            self._check_both_files_loaded()

        except Exception as e:
            logger.error(f"Ошибка обработки файла {file_number}: {e}")
            self._show_message(f"Ошибка загрузки файла {file_number}", Colors.ERROR)

    def _validate_processors(self):
        """Валидация и определение типов таблиц"""

        if not all([self.file1_processor, self.file2_processor]):
            raise ValueError("Не все файлы загружены")

        processors = {
            self.file1_processor.table_name: self.file1_processor,
            self.file2_processor.table_name: self.file2_processor,
        }

        final_domains = processors.get('final_domains')
        dynamics = processors.get('dynamics_collection')

        if not all([final_domains, dynamics]):
            raise ValueError("Не найдены required таблицы final_domains и dynamics_collection")

        return final_domains, dynamics

    def _check_both_files_loaded(self):
        """Проверка готовности обоих файлов и запуск обработки"""
        try:
            if not all([self.file1_processor, self.file2_processor]):
                return
            # self._update_progress()

            final_domains_processor, dynamic_processor = self._validate_processors()

            self.transfer_manager = DataTransferManager(
                final_domains=final_domains_processor.table_data, dynamic=dynamic_processor.table_data
            )

            #result_table = self.transfer_manager.process()

            self._show_message("Таблицы успешно обработаны!")
            self.download_button.disabled = False
            self.download_button.visible = True
            # self.progress_bar.visible = False

            logger.info("Обработка завершена успешно")

        except Exception as e:
            logger.error(f"Ошибка обработки таблиц: {e}")
            # self._show_error(f"Ошибка обработки: {str(e)}")
            # self.progress_bar.visible = False

    def _show_message(self, message: str, color: Colors = Colors.SUCCESS):
        self.notification_container.content = ft.Text(message, color=color)

    def build(self):
        """Построение интерфейса"""

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.TABLE_VIEW, color=ft.Colors.WHITE),
                                self.header_text
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            self.upload_field.display_container,
                            self.upload_field2.display_container,
                            self.notification_container,
                            self.download_button
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER

                    ),
                    margin=ft.margin.only(left=150, right=150, bottom=80),
                    alignment=ft.alignment.center,
                )
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
