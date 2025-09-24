
from pathlib import Path
from rembg import remove
import datetime 

class BackgroundRemover:
    #Variable de clase
    """inicializadores, el self es un atributo que por defecto debe 
    tener en la clase, es una referencia al propio objeto creado a 
    partir de la clase."""
    
    SUPPORTED_EXTENSIONS =(".png",".jpg",".jpeg", ".bmp", ".webp")
    
        #Atributos privados inician con _ ej: _atrbutoPrivado
        #Definir cuerpo del inicializador, ¿Que hara el programa?
    
    def __init__(self, input_folder, output_folder): 
        #Variables de instancia
        self.input_folder = input_folder
        self.output_folder = output_folder
        
    #Esqueleto del programa (Logica para la eliminacion de fondos con responsabilidades)
    
    """Funcion encargada de procesar multiples imagenes para 
    quitar el fondo"""
    def process_images(self, filename_list, proces_callback=None): #Carpeta donde se va aguardar todo: Output/2025-09-10-00-00
        today_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._processed_folder = self.output_folder / today_date
        self._processed_folder.mkdir(parents=True, exist_ok = True)#Creacion de carpeta
        
        total_files = len(filename_list)
        processed = 0
                
        for filename in filename_list:
            if self._is_supported_image(filename):
                input_path = self.input_folder / filename
                output_path = self._processed_folder / filename
                
                
                try:
                    self._remove_backgorund(input_path, output_path)
                    self._move_original(input_path)
                    processed += 1
                except Exception as e:
                    print("Hay un error " +e)
                    
    
    """Funcion de tipo privado que verifica si la extension es
    soportada"""
    def _is_supported_image(self, filename: str):
        return filename.lower().endswith(self.SUPPORTED_EXTENSIONS)
    
    """Funcion privada que se encarga de remover fondos"""
    def _remove_backgorund(self, input_path, output_path ):
        #Context manager: Forma segura de abrir y cerrar recursos
        with open(input_path, "rb") as inp, open(output_path, "wb") as outb:#Entrada donde se le de da la prioridad de "rd" leer binarios y "wb" modificar
            output = remove(inp.read())
            outb.write(output)
    
    
    """Funcion Privada Mover archivo """
    def _move_original(self, input_path):
        
        #Definiendo un path: output/originals
        original_folder = self._processed_folder / "originals"  
        
        #Creacion de carpeta
        original_folder.mkdir(exist_ok = True)
        
        #Creacion de path para guardar la imagen: output/originals/image.png
        new_path = original_folder  / input_path.name 
        input_path.rename(new_path)
#3:05:25

obj = BackgroundRemover(Path(r"C:\Users\LENOVO\Documents\YO\Proyectos Python\App quitar fondo"),Path(r"C:\Users\LENOVO\Documents\YO\Proyectos Python\App quitar fondo\OutputImage"))
obj.process_images(["Jordan.jpg"])