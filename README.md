# Background Remove Pro

Interfaz de escritorio construida con **Flet** que permite eliminar el fondo de imágenes en lote utilizando **rembg** (modelos ONNX). El proyecto organiza el flujo completo: selección de archivos, definición de carpeta de salida, seguimiento de progreso y almacenamiento de originales.

## Características principales
- UI moderna y responsiva con Flet (Python).
- Soporte para múltiples imágenes (PNG, JPG, JPEG, BMP, WEBP).
- Carpeta de salida con marca de tiempo y subcarpeta `originals/` para respaldos.
- Barra de progreso y mensajes contextualizados (éxito/error).
- Configurable para usar carpeta de salida por defecto (`output/`) o una ruta personalizada.

## Stack y dependencias
- **Python 3.12+**
- **Flet** para la interfaz gráfica.
- **rembg** para eliminación de fondos (usa `onnxruntime` y OpenCV).
- `numpy`, `scikit-image`, `pymatting`, `onnxruntime` (instaladas transitivamente por rembg).

## Requisitos previos
- Python 3.12 instalado (`python3 --version`).
- Acceso a internet para instalar dependencias desde PyPI.
- Entorno gráfico disponible para el diálogo de archivos:
  - En Linux: instalar `zenity` (`sudo apt-get install -y zenity`).  
  - En Windows / macOS no es necesario nada extra.

## Instalación
```bash
git clone https://github.com/<tu-usuario>/Background-Remover.git
cd Background-Remover
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install flet rembg onnxruntime
```

### Opcional: guardar dependencias
```bash
pip freeze > requirements.txt
```

## Estructura del proyecto
```
.
├── assets/                 # Recursos estáticos / muestras
├── background_remover/     # Código de la aplicación
│   ├── __init__.py
│   ├── app.py              # Interfaz Flet y lógica de interacción
│   └── processor.py        # Lógica de remoción de fondo
├── main.py                 # Punto de entrada (ejecuta la app)
├── .gitignore
└── README.md
```

## Uso
1. Activa el entorno virtual si no lo has hecho:  
   - Linux/macOS: `source .venv/bin/activate`  
   - Windows (PowerShell): `.venv\Scripts\Activate`
2. Ejecuta la aplicación:  
   ```bash
   python main.py
   ```
3. Flujo en la interfaz:
   - Selecciona imágenes compatibles mediante el botón **Seleccionar imagen**.
   - Define la carpeta de salida (usa la predeterminada `output/` o desmarca el checkbox para ingresar otra ruta).
   - Presiona **Remover fondos** para iniciar el procesamiento. Se generará una carpeta con marca de tiempo dentro de la ruta de salida y un subdirectorio `originals/` con las copias originales.

## Notas y consejos
- Los modelos que usa rembg pueden tardar en descargarse la primera vez; mantén la consola abierta hasta que finalice.
- Si deseas limpiar los resultados, borra el directorio `output/` o la ruta personalizada que hayas usado.
- Para probar rápidamente, coloca imágenes en `assets/samples/` y selecciónalas desde la interfaz.

## Problemas comunes
- **No se abre el selector de archivos en Linux:** asegúrate de tener instalado `zenity`.  
  ```bash
  sudo apt-get install -y zenity
  ```
- **Errores de módulos faltantes:** confirma que el entorno virtual esté activo y que instalaste `rembg` y `onnxruntime` en esa venv.


