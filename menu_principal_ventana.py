import PySimpleGUI as sg
import os
import json
import inicio_ventana
import configuracion
import generador_memes
import editar_perfil
import etiquetar_imagenes
import creador_de_collage

class VentanaMenu:

    '''Metodo que se encarga de preparar la ventana previamente a ser iniciada, recibe un parametro que nos indica que perfil mostrar en pantalla'''
    def __init__(self, perfil_act):
        '''Nos preparamos todas las rutas que vamos a usar en la ventana'''

        current_dir = os.path.abspath(__file__)

        relative_path = "botones/config.png"
        relative_path_2 = "botones/help.png"
        config_img = os.path.join('./', relative_path)
        help_img = os.path.join('./', relative_path_2)

        '''Abrimos el archivo de perfiles, previamente generado, y nos guardamos los mismos'''
        with open('perfil.json', 'r', encoding='utf-8') as archivo: 
            datos = json.load(archivo) #nos guardamos los perfiles del json
        
        for perfil in datos[0:]:
            if (perfil['nick'] == perfil_act):
                perfil_boton = [sg.Button(enable_events=True, key=perfil['nombre'], button_color='white', border_width=0, image_filename=perfil['imagen'])]
                break

        self.perf=perfil_act
        '''Generamos todos los objetos con los que vamos a interactuar en la ventana'''

        etiquetar_imagenes = [sg.Button('Etiquetar Imagenes', key= 'imagenes')]
        generar_meme = [sg.Button('Generar Meme', key= 'meme')]
        generar_collage= [sg.Button('Generar Collage', key='collage')]
        salir = [sg.Button('Salir', key= 'salir')]

        config = [sg.Button(key= 'config', image_filename=config_img, border_width=0, button_color="white", image_subsample=(3))]
        
        
        ayuda = [sg.Button(key= 'help', image_filename=help_img, border_width=0, button_color="white")]

        columna_vacia = [sg.Column([], background_color='white', size=(400,215))]
        columna_vacia2 = [sg.Column([], background_color='white', size=(400,400))]

        column1_layout = [perfil_boton]
        column2_layout = [columna_vacia, etiquetar_imagenes, generar_meme, generar_collage, salir, columna_vacia2]
        column3_layout = [config]
        column4_layout = [ayuda]

        column1 = sg.Column(column1_layout, size=(300, 600), background_color="white")
        column2 = sg.Column(column2_layout, size=(250, 600), background_color="white")
        column3 = sg.Column(column3_layout, size=(82, 600), background_color="white")
        column4 = sg.Column(column4_layout, size=(82, 600), background_color="white")

        layout = [[column1, column2, column3, column4]]
        self.window = sg.Window("UNLP Image", layout, background_color='white', size=(800,600))
    
    '''Metodo que se encarga de iniciar la ventana'''
    def iniciar_ventana(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == 'salir':
                self.window.close()
                inicio = inicio_ventana.VentanaPrincipal()
                inicio.iniciar_ventana()
            elif event == 'config':
                self.window.close()
                self.config=configuracion.Configuracion()
                self.config.abrir_configuracion(self.perf)
            elif event == 'meme':
                self.window.close()
                self.mem= generador_memes.GeneradorMemes()
                self.mem.abrir_ventana(self.perf)
            elif event == 'collage':
                self.window.close()
                self.col = creador_de_collage.ventanaCreador()
                self.col.iniciar_ventana()
            elif event == 'imagenes':
                self.window.close()
                self.img = etiquetar_imagenes.ventanaEtiquetar()
                self.col.iniciar_ventana()
            elif event == 'help':
                sg.Popup('''Esta ventana proporciona una navegación fluida entre las diferentes funcionalidades de la aplicación. En la parte superior de la ventana,
                 se mostrará el perfil seleccionado, incluyendo su avatar y nombre. Al hacer clic en la imagen del perfil, se desplegará la ventana para editar el perfil (D - Editar perfil). 
                 El menú de opciones se encuentra en la parte inferior de la pantalla, y ofrece acceso a las funcionalidades principales de la aplicación. 
                 La configuración se puede acceder a través del botón correspondiente.''', 
                 title='Ayuda')
            else:
                self.window.close()
                self.edit=editar_perfil.EditarPerfil(self.perf)
                self.edit.iniciar_ventana(self.perf)
                
        self.window.close()