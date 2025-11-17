from pathlib import Path

import flet as ft

from excel_data_processor import ExcelDataProcessor
from typing import Optional, Callable
import logging
from colors import Colors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__file__)


class ExcelUploadField:
    """Компонент для загрузки Excel файлов с валидацией и уведомлениями"""

    def __init__(
            self, file_picker: ft.FilePicker,
            notification_container: ft.Container,
            on_file_loaded: Callable[[ExcelDataProcessor], None]
    ):
        self.file_picker = file_picker
        self.notification_container = notification_container
        self.on_file_loaded = on_file_loaded
        self.processor: Optional[ExcelDataProcessor] = None

        self._set_up_ui()

    def _set_up_ui(self):
        """Настройка пользовательского интерфейса компонента"""
        self.path_text = ft.Text(
            "Файл не выбран",
            color=Colors.SECONDARY_COLOR,
            size=14,
            expand=True
        )

        self.select_button = ft.ElevatedButton(
            text="Выбрать файл",
            on_click=self._on_pick_file
        )

        self.file_path_display = ft.Container(
            content=ft.Row([
                self.path_text,
                self.select_button
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=12,
            border=ft.border.all(1.1, Colors.DEFAULT_BORDER_COLOR),
            border_radius=15,
        )

    def _connect_file_picker(self):
        """Подключение обработчика FilePicker"""
        self.file_picker.on_result = self._handle_file_pick

    def _on_pick_file(self, event: ft.ControlEvent):
        """Обработчик нажатия кнопки выбора файла"""
        try:
            self._connect_file_picker()

            self.file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=['xls', 'xlsx']
            )

        except Exception as e:
            logger.error(f"Ошибка при выборе файла: {e}")
            # self._show_error_message("Ошибка при выборе файла")

    def _show_message(self, message: str, color: Colors = Colors.SUCCESS):
        """Показать сообщение в контейнере уведомлений"""
        try:
            self.notification_container.content = ft.Text(
                value=message,
                size=14,
                expand=True,
                color=color
            )

            self.notification_container.alignment = ft.alignment.center_left
            self.notification_container.padding = ft.padding.symmetric(horizontal=12)
            self.notification_container.visible = True
            self.notification_container.update()

        except Exception as e:
            logger.error(f"Ошибка при отображении сообщения: {e}")

    def _show_error_message(self, message: str) -> None:
        """Показать сообщение об ошибке."""
        self._show_message(message, color=Colors.ERROR)

    def _set_file_path(self, file):
        display_path = file.path
        self.path_text.value = display_path
        self.path_text.color = Colors.PATH_TEXT_COLOR
        self.file_path_display.border = ft.border.all(1, color=Colors.SUCCESS)
        self.file_path_display.update()

    def _process_file(self, file_path: str):
        """Обработка выбранного файла"""

        #try:
        logger.info(f"Начало обработки файла: {file_path}")

        self.processor = ExcelDataProcessor(file_path)
        processed_data = self.processor.process_table()


        logger.info(f"Файл успешно обработан: {file_path}")
        self._show_message(f"Таблица {Path(file_path).name} успешно загружена и обработана!")

        # Вызов колбэка с передачей процессора
        self.on_file_loaded(self.processor)

        #except Exception as e:
            ##self._show_error_message(f"Ошибка при обработке файла: {str(e)}")
            #raise

    def _handle_file_pick(self, event: ft.FilePickerResultEvent):
        if not event.files:
            logger.debug("Выбор файла отменен")
            return

        #try:
        file = event.files[0]
        logger.info(f"Выбран файл: {file.name}")
        self._show_progress()
        self._set_file_path(file)
        self._process_file(file.path or file.name)

        #except Exception as e:
            #logger.error(f"Критическая ошибка при обработке выбора файла: {e}")
            #self._show_error_message("Критическая ошибка при загрузке файла")

    def _show_progress(self):
        self.notification_container.content = ft.ProgressBar(
            width=600,
            height=2,
            color=Colors.SUCCESS,
            bgcolor=Colors.SECONDARY_COLOR
        )
        self.notification_container.alignment = ft.alignment.center
        self.notification_container.margin = ft.margin.only(top=5)
        self.notification_container.visible = True
        self.notification_container.update()

    @property
    def display_container(self) -> ft.Container:
        """Контейнер для отображения в UI"""
        return self.file_path_display
