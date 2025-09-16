import flet  as ft
def main(page: ft.Page):
    page.title = "Backgorund Remove Pro"#Nombre de la aplicacion
    page.bgcolor = "#1a1a2e" #Fondo de la app
    page.window.height = 900 #Altura de la ventana
    page.window.width = 700 #Ancho de a ventana 
    page.theme_mode = ft.ThemeMode.DARK
     
    btn_simple = ft.ElevatedButton(# Creacion de boton para la interfaz 
        text="Seleccionar Imagenes",
        on_click=lambda p: print("Hola mundo") #Lambda Funtion, funcion anonima
    )
    
    btn_with_style = ft.ElevatedButton(
        text="Seleccionar Imágenes",
        bgcolor="#0f3460",
        color='#ffffff',
        width=250,
        height=50
    )
    
    btn_profesional = ft.ElevatedButton(
        bgcolor="#0f3460",
        color='#ffffff',
        width=250,
        height=50,
        content=ft.Row([
            ft.Icon(ft.Icons.CLOUD_UPLOAD, color="#ffffff"),#Se importa la imagen de una nube 
            ft.Text("Seleccionar Imágen", color="#ffffff", weight=ft.FontWeight.BOLD) #Se agrega negrilla al texto
        ], alignment=ft.MainAxisAlignment.CENTER),#Los elementos se alinean al centro
        style=ft.ButtonStyle( #Gregarle mas estilos al boton
            shape=ft.RoundedRectangleBorder(radius=12), #Se agrega bordes rectangulares con un radio de 12 
            elevation=5 #Efecto sombra
        )
    )
    
    
    page.add(btn_simple,
             btn_with_style,
             btn_profesional) #Se añaden los elementos creados a la interfaz

ft.app(target=main)

#1:01:27