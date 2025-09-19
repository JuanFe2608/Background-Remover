import flet  as ft
import os


def main(page: ft.Page):
    page.title = "Backgorund Remove Pro"#Nombre de la aplicacion
    page.bgcolor = "#1a1a2e" #Fondo de la app
    page.window.height = 900 #Altura de la ventana
    page.window.width = 700 #Ancho de a ventana 
    page.theme_mode = ft.ThemeMode.DARK
    
    #Cracion de control
    output_folder_textfield =ft.TextField(
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
    
    #Funcion para que cuando se seleccione el CheckBox de usar carpeta por defecto se desactive la opcion para poner la carpeta
    def _checkbox_changed(e:ft.ControlEvent):#Funcion de tipo privado
        output_folder_textfield.disabled = e.control.value #Poner en valor en el output_folder_textfield de acuerdo al control de evento que me pasa el checkbox
        output_folder_textfield.bgcolor = "#2a2a40" if e.control.value else "#16213e"
        page.update()
    
    #Creacion de un CheckBox
    default_folder_check = ft.Checkbox(
        label = "Usar carpeta por defecto", #Texto del checkbox
        value = False,#Valor predeterminado en el que empieza el checkbox
        on_change = _checkbox_changed, #Al seleccionar el checkbox se hace la accion que determina la funcion
        check_color ='#e94560',
        label_style= ft.TextStyle(color="#ffffff", size=14),#Estilo al label definido
    ) #Variable que almacena un objeto de tipo checkbox
    
    
    select_files_info = ft.Text(#Clase que me cre objetos de tipo texto, las clases siempre van en mayuscula en la inicial
        "Ningun archivo ha sido seleccionado",
        color="#a0a0a0",
        size=14,
    )
    
    def pick_files_result(e: ft.FilePickerResultEvent): #Creacion de funcion usando Type Hinting para cuando se selecione cualquier elemento
        if e.files:
            file_count=len(e.files)#Capturar el numero de archivos que selecciono el usuario
            first_file_path = e.files[0].path#La ruta completa que representa el primer archivo
            directory = os.path.dirname(first_file_path)#Obteniendo el nombre del directorio de la primera ruta que le pasamos
            
            select_files_info.value = f" {file_count} Archivo(s) seleccionados \nCarpeta: {directory} " #Se modifica el estado del objeto select_files_info cuando se agregan archivos
            
            select_files_info.color = "#4caf50"
        else: 
            select_files_info.value = "Selesccion Cancelada"
            select_files_info.color = "#f44336"
            
        page.update()
        
    #Creacion Filepicker
        
    file_picker = ft.FilePicker(on_result=pick_files_result)#Selector de archivos
    page.overlay.append(file_picker)#Se usa para agregar un control encima de la interfaz principal.
    
    #Creacion Boton
    btn_pick_files = ft.ElevatedButton(
        bgcolor="#0f3460",
        color='#ffffff',
        width=250,
        height=50,
        content=ft.Row([
            ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),#Se importa la imagen de una nube 
            ft.Text("Seleccionar Imágen", color="#ffffff", weight=ft.FontWeight.BOLD) #Se agrega negrilla al texto
        ], alignment=ft.MainAxisAlignment.CENTER),#Los elementos se alinean al centro
        on_click=lambda _ : file_picker.pick_files(#activamos el file picker, el "_es porque no nos interesan los parametros que nos estan dando y esa usa por convencion"
            allow_multiple=True,
            allowed_extensions=["png","jpg", "jpeg", "bmp", "webp"]
        ),
        style=ft.ButtonStyle( #Agregarle mas estilos al boton
            shape=ft.RoundedRectangleBorder(radius=12), #Se agrega bordes rectangulares con un radio de 12 
            elevation=5 #Efecto sombra
        )
    )
    
    #Creacion de boton para quitar boton 
    btn_extract = ft.ElevatedButton(
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
    
    #Card de configuracion
    #Un container es un control que me permite almacenar o organizar diferentes coumnas
    config_card = ft.Container(
        content=ft.Column([#Layout Tipo columna que a su vez almacena un layout de tipo row
            ft.Row([
                ft.Icon(ft.Icons.SETTINGS, color="#e94560",size=20),
                ft.Text("Configuración", weight=ft.FontWeight.BOLD,color="#ffffff", size=18)
            ], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=10),
            default_folder_check,
            ft.Container(height=10),
            output_folder_textfield,
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
                btn_pick_files,
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            select_files_info,
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
            btn_extract,
            ft.Container(height=15),
        ], horizontal_alignment= ft.CrossAxisAlignment.CENTER),
        bgcolor="#16213e",
        padding=ft.padding.all(20),
        border_radius=15,
        border=ft.border.all(1, "#0f3460"),
        width=600
    )
    
     
    page.add(config_card,
             files_card,
             process_card,
             )

ft.app(target=main)#El metodo app apunta a la funcion main

#2:37:53
