import flet as ft
import os 

class BackgroundRemoverApp:
    
    #Metodo inicializador, es el primer metodo que se jecuta automaticamente.
    """Todos lo metodos agregados a una clase reciben un argumento por defecto 
    que hace referecnia a su propia clase (self), se usa unicamente 
    para referenciar objetos o funciones que estan dentro de la clase """
    
    def __init__(self, page: ft.Page):
        
        #Variables de instancia
       '''self.nombre_de_la_variable_de_instancia = argumento que me esta pasando la funcion''' 
       self.page = page #Creacion objeto tipo page
       #Variable de instancia para guardar el directorio de as imagenes
       self.directory_path = None
       self.filename_list = [] 
       self._setup_page()
       self._create_components()
       self._build_ui()
       
       
    #Separacion de responsabilidades.
    
    def _setup_page(self):
        self.page.title = "Backgorund Remove Pro"#Nombre de la aplicacion
        self.page.bgcolor = "#1a1a2e" #Fondo de la app
        self.page.window.height = 900 #Altura de la ventana
        self.page.window.width = 700 #Ancho de a ventana 
        self.page.theme_mode = ft.ThemeMode.DARK
    
    def _create_components(self):
        #Creacion de un CheckBox
        self.default_folder_check = ft.Checkbox(
            label = "Usar carpeta por defecto", #Texto del checkbox
            value = False,#Valor predeterminado en el que empieza el checkbox
            on_change = self._checkbox_changed, #Al seleccionar el checkbox se hace la accion que determina la funcion
            check_color ='#e94560',
            label_style= ft.TextStyle(color="#ffffff", size=14),#Estilo al label definido
        ) #Variable que almacena un objeto de tipo checkbox
        
        #Creacion de un textfield
        self.output_folder_textfield =ft.TextField(
            label="Carpeta de salida personalizada",
            autofocus= False,#No tenga el foco automaticamente al crear nuestra app en flet
            bgcolor="#16213e",
            color="#ffffff",
            border_color="#0f3460",
            focused_border_color="#e94560",
            width=350,
            height=60,
            border_radius=10,
            content_padding=ft.padding.all(15),
        )
        
        self.file_picker = ft.FilePicker(on_result=self.pick_files_result)
        
        #Creacion Boton
        self.btn_pick_files = ft.ElevatedButton(
            bgcolor="#0f3460",
            color='#ffffff',
            width=250,
            height=50,
            content=ft.Row([
                ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),#Se importa la imagen de una nube 
                ft.Text("Seleccionar Imágen", color="#ffffff", weight=ft.FontWeight.BOLD) #Se agrega negrilla al texto
            ], alignment=ft.MainAxisAlignment.CENTER),#Los elementos se alinean al centro
            on_click=lambda _ : self.file_picker.pick_files(#activamos el file picker, el "_es porque no nos interesan los parametros que nos estan dando y esa usa por convencion"
                allow_multiple=True,
                allowed_extensions=["png","jpg", "jpeg", "bmp", "webp"]
            ),
            style=ft.ButtonStyle( #Agregarle mas estilos al boton
                shape=ft.RoundedRectangleBorder(radius=12), #Se agrega bordes rectangulares con un radio de 12 
                elevation=5 #Efecto sombra
            )
        )
        
        self.select_files_info = ft.Text(#Clase que me crea objetos de tipo texto, las clases siempre van en mayuscula en la inicial
            "Ningun archivo ha sido seleccionado",
            color="#a0a0a0",
            size=14,
        )
        
        #Creacion boton para extraer elementos
        self.btn_extract = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.Icons.AUTO_FIX_HIGH,color="#ffffff"),
                ft.Text("Remover Fondos", color="#ffffff", size=16, weight=ft.FontWeight.BOLD)
            ], alignment= ft.MainAxisAlignment.CENTER),
            on_click= lambda _: print("hola"),
            bgcolor="#e94560",
            color="#ffffff",
            width=300,
            height=60,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=15),
                elevation=8     
            )
        )
    
        self.page.overlay.append(self.file_picker)#Se usa para agregar un control encima de la interfaz principal.
        
    def _build_ui(self):
        #Card de configuracion
        #Un container es un control que me permite almacenar o organizar diferentes coumnas
        config_card = ft.Container(
            content=ft.Column([#Layout Tipo columna que a su vez almacena un layout de tipo row
                ft.Row([
                    ft.Icon(ft.Icons.SETTINGS, color="#e94560",size=20),
                    ft.Text("Configuración", weight=ft.FontWeight.BOLD,color="#ffffff", size=18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=10),
                self.default_folder_check,
                ft.Container(height=10),
                self.output_folder_textfield,
            ], spacing=5),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
            width=600
        )
        
        #Card de archivos
        
        files_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.IMAGE, color="#e94560", size=20),
                    ft.Text("Seleccionar Archivos", weight=ft.FontWeight.BOLD, color="ffffff", size= 18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=15),
                ft.Row([
                    self.btn_pick_files,
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                self.select_files_info,
            ], horizontal_alignment= ft.CrossAxisAlignment.CENTER),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
            width=600
        )
        
        process_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, color="#e94560", size=20),
                    ft.Text("Procesamiento", weight=ft.FontWeight.BOLD, color="ffffff", size= 18)
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                self.btn_extract,
                ft.Container(height=15),
            ], horizontal_alignment= ft.CrossAxisAlignment.CENTER),
            bgcolor="#16213e",
            padding=ft.padding.all(20),
            border_radius=15,
            border=ft.border.all(1, "#0f3460"),
            width=600
        )
        
        self.page.add(config_card,
             files_card,
             process_card,
             )
        
    
        #Funcion para que cuando se seleccione el CheckBox de usar carpeta por defecto se desactive la opcion para poner la carpeta
    
    def _checkbox_changed(self, e:ft.ControlEvent):#Funcion de tipo privado
        self.output_folder_textfield.disabled = e.control.value #Poner en valor en el output_folder_textfield de acuerdo al control de evento que me pasa el checkbox
        self.output_folder_textfield.bgcolor = "#2a2a40" if e.control.value else "#16213e"
        self.page.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent): #Creacion de funcion usando Type Hinting para cuando se selecione cualquier elemento
        if e.files:
            file_count=len(e.files)#Capturar el numero de archivos que selecciono el usuario
            first_file_path = e.files[0].path#La ruta completa que representa el primer archivo
            directory = os.path.dirname(first_file_path)#Obteniendo el nombre del directorio de la primera ruta que le pasamos
            
            self.select_files_info.value = f" {file_count} Archivo(s) seleccionados \nCarpeta: {directory} " #Se modifica el estado del objeto select_files_info cuando se agregan archivos
            
            self.select_files_info.color = "#4caf50"
        else: 
            self.select_files_info.value = "Selesccion Cancelada"
            self.select_files_info.color = "#f44336"
            
        self.page.update()
    
def main(page:ft.Page):
    obj = BackgroundRemoverApp(page)
    
ft.app(target=main)

