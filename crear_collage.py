import PySimpleGUI as sg
import os.path
import json
import datetime
import csv
import creador_de_collage

class VentanaCollage:

    def __init__(self):
        #Inicializa la clase del creador de collage

        def create_folder_input(texto):
            '''Crea un campo de entrada de carpeta con un botón de selección.

            Recibe: texto: El texto que se mostrará junto al campo de entrada.

            Devuelve: El campo de entrada y el botón de selección empaquetados en una columna.'''
            return sg.Column([
                [sg.Text(texto, font=('Arial', 12), background_color='white', text_color='black')],
                [sg.In(size=(25, 1), enable_events=True, key=texto),
                 sg.FolderBrowse(button_text='Seleccionar', button_color='black')],
                [sg.Text('', size=(1, 10), background_color='white')]], size=(450, 90), background_color='white')
        espacio1 = [sg.Text('', size=(1, 25), background_color='white')]
        titulo = [sg.Text('Generar collage', font=('Arial'), background_color='white', text_color='black')]
        textos = ['Seleccionar imagen 1', 'Seleccionar imagen 2', 'Seleccionar imagen 3']
        columnas = [create_folder_input(textos[i]) for i in range(3)]
        col = sg.Column([] + [[col] for col in columnas], size=(450, 600),background_color='white')

        relative_path = "botones\\botonVolver2.png"
        relative_path2 = "botones\\salvar.png"

        boton_volver = os.path.join('./', relative_path)
        boton_guardar = os.path.join('./', relative_path2)
    
        boton_volver = [sg.Button(enable_events=True, image_subsample=(10), button_color='white', border_width=0,
                                  image_size=(50, 50), image_filename=boton_volver, key='VOLVER')]
        boton_guardar = [sg.Button(image_size=(50, 50), image_filename=boton_guardar, button_color='white',
                                   enable_events=True, border_width=0, image_subsample=(9), key='GUARDAR')] 
        elem_col2 = [boton_volver, espacio1, boton_guardar]
        width, height = 100, 100
     
        col2 = sg.Column(elem_col2)

        layout1 = [[titulo, col, col2]]
        self.window = sg.Window('UNLPImage', background_color='white', element_padding=(0, 3), size=(800, 600),layout=layout1)

    def iniciar_ventana(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Salir':
                break 
            elif event == 'VOLVER':
                self.window.close()
                volver = creador_de_collage.ventanaCreador()
                volver.iniciar_ventana()
                
        self.window.close()