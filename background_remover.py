
from pathlib import Path
from rembg import remove

class BackgroundRemover:
    #Variable de clase
    SUPPORTED_EXTENSIONS =(".png",".jpg",".jpeg", ".bmp", ".webp")
    
    
    def __init__(self, input_folder, output_folder): #inicializadores, el self es un atributo qu epor defecto debe tener en la clase, es una referencia al propio objeto creado a partit de la clase.
        #Atrbutos privados inician con _ ej: _atrbutoPrivado
        
        #Definir cuerpo del inicializador, ¿Que hara el programa?
        
        #Variables de instancia
        self.input_folder = input_folder
        self.output_folder = output_folder
    
    def removeBackground(self, input_folder, output_folder):
        #Context Manager = Abrir recursos utilizarlos y cerrarlos automaticamente
        #Creacion de Context Manager
        with open(input_folder, 'rb') as inp, open(output_folder, 'wb') as outp: #Estamos creando los context manager con la funcion de open "rb" leer en binario "rb "y escribir en binario "wb" 
        
            output = remove(inp.read()) #Con la importacion de remove le pasamos la ruta en input_folder de nuestra imagen para que luego borre el fondo y lo guarde en la variable output
            outp.write(output)
        
#Instancia de la clase BackgroundRemove
remover = BackgroundRemover('input1.jpg','input2.jpg')
remover.removeBackground("Jordan.jpg",'Jordan_WithoutBackground.jpg') #Ruta parcial, ruta completa
