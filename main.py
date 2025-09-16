import flet  as ft
import os


def main(page: ft.Page):
    page.title = "Backgorund Remove Pro"#Nombre de la aplicacion
    page.bgcolor = "#1a1a2e" #Fondo de la app
    page.window.height = 900 #Altura de la ventana
    page.window.width = 700 #Ancho de a ventana 
    page.theme_mode = ft.ThemeMode.DARK
    
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
        style=ft.ButtonStyle( #Gregarle mas estilos al boton
            shape=ft.RoundedRectangleBorder(radius=12), #Se agrega bordes rectangulares con un radio de 12 
            elevation=5 #Efecto sombra
        )
    )
     
     
    page.add(select_files_info,btn_pick_files)

ft.app(target=main)#El metodo app apunta a la funcion main

#1:31:44