from __future__ import annotations

from pathlib import Path
from typing import Optional

import flet as ft

from .processor import BackgroundRemover

DEFAULT_OUTPUT_DIR = "output"

COLOR_BACKGROUND = "#0f172a"
COLOR_SURFACE = "#17223b"
COLOR_SURFACE_ALT = "#1f2a44"
COLOR_BORDER = "#23304d"
COLOR_ACCENT = "#38bdf8"
COLOR_ACCENT_ALT = "#fbbf24"
COLOR_TEXT_PRIMARY = "#e2e8f0"
COLOR_TEXT_SECONDARY = "#94a3b8"
COLOR_ERROR = "#f87171"
COLOR_SUCCESS = "#34d399"
COLOR_DISABLED = "#475569"


class BackgroundRemoverApp:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.directory_path: Optional[Path] = None
        self.selected_filenames: list[str] = []

        self._setup_page()
        self._create_components()
        self._build_ui()

    def _setup_page(self) -> None:
        self.page.title = "Background Remove Pro"
        self.page.bgcolor = COLOR_BACKGROUND
        self.page.window.height = 720
        self.page.window.width = 960
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.scroll = ft.ScrollMode.AUTO

    def _create_components(self) -> None:
        self.default_folder_check = ft.Checkbox(
            label="Usar carpeta por defecto",
            value=True,
            on_change=self._checkbox_changed,
            check_color=COLOR_ACCENT,
            label_style=ft.TextStyle(color=COLOR_TEXT_PRIMARY, size=14),
        )

        self.output_folder_textfield = ft.TextField(
            label="Carpeta de salida personalizada",
            autofocus=False,
            bgcolor=COLOR_SURFACE_ALT,
            color=COLOR_TEXT_PRIMARY,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_ACCENT,
            cursor_color=COLOR_ACCENT,
            selection_color="#1f2937",
            width=360,
            height=60,
            border_radius=12,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            disabled=True,
            value=DEFAULT_OUTPUT_DIR,
        )

        self.file_picker = ft.FilePicker(on_result=self._pick_files_result)
        self.page.overlay.append(self.file_picker)

        self.btn_pick_files = ft.ElevatedButton(
            bgcolor=COLOR_SURFACE_ALT,
            color=COLOR_TEXT_PRIMARY,
            width=260,
            height=52,
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.CLOUD_UPLOAD, color=COLOR_ACCENT),
                    ft.Text("Seleccionar imagen", color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=lambda _: self.file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["png", "jpg", "jpeg", "bmp", "webp"],
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=14),
                elevation=4,
            ),
        )

        self.select_files_info = ft.Text(
            "Ningún archivo ha sido seleccionado",
            color=COLOR_TEXT_SECONDARY,
            size=14,
            text_align=ft.TextAlign.CENTER,
        )

        self.btn_extract = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.AUTO_FIX_HIGH, color=COLOR_TEXT_PRIMARY),
                    ft.Text("Remover fondos", color=COLOR_TEXT_PRIMARY, size=16, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=self._process_images_ui,
            bgcolor=COLOR_ACCENT_ALT,
            color=COLOR_TEXT_PRIMARY,
            width=320,
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                elevation=8,
            ),
        )

        self.progress_bar = ft.ProgressBar(
            value=0,
            visible=False,
            color=COLOR_ACCENT,
            bgcolor=COLOR_SURFACE_ALT,
            height=6,
            expand=True,
        )

        self.progress_text = ft.Text(
            "",
            visible=False,
            color=COLOR_TEXT_PRIMARY,
            size=14,
            text_align=ft.TextAlign.CENTER,
        )

    def _build_ui(self) -> None:
        def build_card(icon: str, title: str, controls: list[ft.Control]) -> ft.Container:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(icon, color=COLOR_ACCENT, size=22),
                                ft.Text(title, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY, size=18),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(height=12),
                        *controls,
                    ],
                    spacing=12,
                ),
                bgcolor=COLOR_SURFACE,
                padding=ft.padding.symmetric(horizontal=24, vertical=22),
                border_radius=18,
                border=ft.border.all(1, COLOR_BORDER),
                expand=True,
            )

        header = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Background Remove Pro", size=28, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                    ft.Text(
                        "Organiza tus archivos, define la salida y procesa los fondos en un solo flujo.",
                        size=15,
                        color=COLOR_TEXT_SECONDARY,
                    ),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.only(bottom=24),
        )

        config_card = build_card(
            ft.Icons.SETTINGS,
            "Configuración",
            [
                self.default_folder_check,
                ft.Container(height=10),
                self.output_folder_textfield,
                ft.Text(
                    "La carpeta por defecto se creará dentro de tu proyecto como /output.",
                    size=12,
                    color=COLOR_TEXT_SECONDARY,
                ),
            ],
        )

        files_card = build_card(
            ft.Icons.FOLDER_OPEN,
            "Archivos de entrada",
            [
                ft.Text(
                    "Selecciona una o varias imágenes compatibles (PNG, JPG, JPEG, BMP, WEBP).",
                    size=13,
                    color=COLOR_TEXT_SECONDARY,
                ),
                ft.Row([self.btn_pick_files], alignment=ft.MainAxisAlignment.START),
                self.select_files_info,
            ],
        )

        process_card = build_card(
            ft.Icons.PLAY_CIRCLE,
            "Procesamiento",
            [
                ft.Text(
                    "Revisa la configuración y presiona el botón para iniciar el procesamiento en lote.",
                    size=13,
                    color=COLOR_TEXT_SECONDARY,
                ),
                ft.Row([self.btn_extract], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=8),
                self.progress_bar,
                self.progress_text,
            ],
        )

        left_column = ft.Column(
            [config_card, files_card],
            spacing=20,
            expand=2,
        )

        right_column = ft.Column(
            [process_card],
            spacing=20,
            expand=1,
        )

        body = ft.Row(
            [
                ft.Container(content=left_column, expand=2),
                ft.Container(content=right_column, expand=1),
            ],
            spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        wrapper = ft.Container(
            content=ft.Column([header, body], spacing=0, expand=True),
            padding=ft.padding.symmetric(horizontal=36, vertical=32),
            expand=True,
        )

        self.page.add(wrapper)

    def _checkbox_changed(self, event: ft.ControlEvent) -> None:
        use_default = event.control.value
        self.output_folder_textfield.disabled = use_default
        self.output_folder_textfield.bgcolor = COLOR_SURFACE_ALT if use_default else COLOR_SURFACE
        if use_default:
            self.output_folder_textfield.value = DEFAULT_OUTPUT_DIR
        self.page.update()

    def _pick_files_result(self, event: ft.FilePickerResultEvent) -> None:
        if not event.files:
            self.select_files_info.value = "Selección cancelada"
            self.select_files_info.color = COLOR_ERROR
            self.selected_filenames = []
            self.directory_path = None
            self.page.update()
            return

        valid_paths = [Path(file.path) for file in event.files if file.path]
        if not valid_paths:
            self.select_files_info.value = "No se pudo leer la ruta de los archivos seleccionados"
            self.select_files_info.color = COLOR_ERROR
            self.selected_filenames = []
            self.directory_path = None
            self.page.update()
            return

        self.directory_path = valid_paths[0].parent
        self.selected_filenames = [path.name for path in valid_paths]

        self.select_files_info.value = (
            f"{len(self.selected_filenames)} archivo(s) seleccionados\nCarpeta: {self.directory_path}"
        )
        self.select_files_info.color = COLOR_SUCCESS
        self.page.update()

    def _process_images_ui(self, _: ft.ControlEvent) -> None:
        if not self.selected_filenames or not self.directory_path:
            self._show_error("Selecciona al menos un archivo antes de procesar.")
            return

        output_folder = (
            Path(DEFAULT_OUTPUT_DIR)
            if self.default_folder_check.value
            else Path(self.output_folder_textfield.value or "").expanduser()
        )

        if not str(output_folder).strip():
            self._show_error("Por favor especifica una carpeta de salida.")
            return

        self._set_processing_state(True)

        try:
            remover = BackgroundRemover(self.directory_path, output_folder)
            remover.process_images(self.selected_filenames, self._update_progress)
            self._show_success("Las imágenes fueron procesadas correctamente.")
        except Exception as exc:
            self._show_error(f"Ha ocurrido un error: {exc}")
        finally:
            self._set_processing_state(False)

    def _set_processing_state(self, processing: bool) -> None:
        self.btn_extract.disabled = processing
        self.btn_extract.bgcolor = COLOR_DISABLED if processing else COLOR_ACCENT_ALT
        self.progress_bar.visible = processing
        self.progress_text.visible = processing
        if processing:
            self.progress_bar.value = 0
            self.progress_text.value = "Iniciando procesamiento..."
            self.progress_text.color = COLOR_TEXT_PRIMARY
        self.page.update()

    def _update_progress(
        self,
        processed: int,
        total: int,
        current_file: str,
        error: Optional[str] = None,
    ) -> None:
        if error:
            self.progress_text.value = f"Error con {current_file}: {error}"
            self.progress_text.color = COLOR_ERROR
        else:
            progress = processed / total if total else 0
            self.progress_bar.value = progress
            self.progress_text.value = f"Procesando: {current_file} ({processed}/{total})"
            self.progress_text.color = COLOR_TEXT_PRIMARY
        self.page.update()

    def _show_error(self, message: str) -> None:
        self._open_dialog("Error", message, COLOR_ERROR)

    def _show_success(self, message: str) -> None:
        self._open_dialog("¡Éxito!", message, COLOR_SUCCESS)

    def _open_dialog(self, title: str, message: str, accent_color: str) -> None:
        dialog = ft.AlertDialog(
            title=ft.Text(title, color=accent_color),
            content=ft.Text(message, color=COLOR_TEXT_PRIMARY),
            bgcolor=COLOR_SURFACE,
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda _: self.page.close(dialog),
                    style=ft.ButtonStyle(color=accent_color),
                )
            ],
        )
        self.page.open(dialog)


def main(page: ft.Page) -> None:
    BackgroundRemoverApp(page)


def run() -> None:
    ft.app(target=main)


if __name__ == "__main__":
    run()
