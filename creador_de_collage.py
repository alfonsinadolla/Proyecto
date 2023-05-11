import PySimpleGUI as sg
import menu_principal_ventana

class ventanaCreador:
    def __init__(self, perfil_act):
        # Crear una lista de elementos
        elementos = [[sg.Button('Etiqueta 1',size=(25,4),pad=((0,0),(0,20)))],
                [sg.Button('Etiqueta 2',size=(25,4),pad=((0,0),(0,20)))],
                [sg.Button('Etiqueta 3',size=(25,4),pad=((0,0),(0,20)))],
                [sg.Button('Etiqueta 4',size=(25,4),pad=((0,0),(0,20)))]]

        # Crear la ventana y agregar la columna a la misma

        left_col =[[sg.Text('Bienvenido al Creador de Collage',pad=((20,0),(0,100)))],
                [sg.Column(elementos,pad=((20,1),(10,0)))]]

        right_col = [[sg.Push(),sg.Button('Volver',key='volver',size=(10,2))],
                [sg.Text('Aquí va el collage',text_color='black', font=('Helvetica', 10), background_color='white',size=(30,20),pad=((200,0),(80,20)))],
                [sg.Button('Generar collage',size=(10,2),pad=((400,0),(0,20)))],
                [sg.Push(),sg.Button('Salir',size=(10,2))]]

        layout = [[sg.Column(left_col), sg.Column(right_col)]]

        window = sg.Window('Creador de Collage', layout, size=(800,600))

    def iniciar_ventana(self):
        # Event Loop
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Salir':
                break 
            elif event == 'volver' or event == sg.WIN_CLOSED:
                menu = menu_principal_ventana.VentanaMenu()
                menu.iniciar_ventana()
        self.window.close()
