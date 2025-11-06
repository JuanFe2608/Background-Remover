
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, Optional

from rembg import remove

ProgressCallback = Callable[[int, int, str, Optional[str]], None]


class BackgroundRemover:
    """Procesa imágenes y elimina el fondo utilizando rembg."""

    SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    def __init__(self, input_folder: Path, output_folder: Path) -> None:
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)

    def process_images(
        self,
        filename_list: Iterable[str],
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        supported_files = [
            filename for filename in filename_list if self._is_supported_image(filename)
        ]
        total_files = len(supported_files)
        if total_files == 0:
            return

        processed_folder = self._create_processed_folder()
        originals_folder = processed_folder / "originals"
        originals_folder.mkdir(exist_ok=True)

        processed = 0

        for filename in supported_files:
            input_path = self.input_folder / filename
            output_path = processed_folder / filename

            if not input_path.exists():
                self._notify(progress_callback, processed, total_files, filename, "Archivo no encontrado")
                continue

            try:
                self._remove_background(input_path, output_path)
                self._move_original(input_path, originals_folder)
                processed += 1
                self._notify(progress_callback, processed, total_files, filename)
            except Exception as exc:  # pragma: no cover - rembg levanta múltiples excepciones
                self._notify(progress_callback, processed, total_files, filename, str(exc))

    def _create_processed_folder(self) -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        processed_folder = self.output_folder / timestamp
        processed_folder.mkdir(parents=True, exist_ok=True)
        return processed_folder

    def _is_supported_image(self, filename: str) -> bool:
        return filename.lower().endswith(self.SUPPORTED_EXTENSIONS)

    def _remove_background(self, input_path: Path, output_path: Path) -> None:
        with input_path.open("rb") as source, output_path.open("wb") as destination:
            destination.write(remove(source.read()))

    def _move_original(self, input_path: Path, originals_folder: Path) -> None:
        input_path.rename(originals_folder / input_path.name)

    def _notify(
        self,
        progress_callback: ProgressCallback | None,
        processed: int,
        total_files: int,
        filename: str,
        error: Optional[str] = None,
    ) -> None:
        if progress_callback:
            progress_callback(processed, total_files, filename, error)
