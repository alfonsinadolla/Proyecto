import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
import csv
import datetime
import menu_principal_ventana


class ventanaEtiquetar:

    def __init__(self):
        left_col = [[sg.Text('Bienvenido a Etiquetar Imagenes')],
                    [sg.Text('Folder'), sg.In(
                        size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
                    [sg.Listbox(values=[], enable_events=True,
                                size=(40, 20), key='-FILE LIST-')],
                    [sg.Text('Tags')],
                    [sg.Input(key='-TAGS-'),
                     sg.Button('Agregar', key='AgregarTags')],
                    [sg.Text('Descripción')],
                    [sg.Input(key='-DESC-'), sg.Button('Agregar', key='AgregarDesc')]]

        right_col = [[sg.Button('Volver', size=(10, 2), pad=((280, 0), (0, 0)))],
                     [sg.Text(size=(40, 1), key='-TOUT-')],
                     [sg.Image(key='-IMAGE-', size=(340, 340))],
                     [sg.Text('Tamaño:', key='-TAMAÑO-')],
                     [sg.Text('Tipo:', key='-TIPO-')],
                     [sg.Text('Resolucion:', key=('-RESOLUCION-'))],
                     [sg.Text("", key="-TAGVALUE-")],
                     [sg.Text("", key="-DESCVALUE-")],
                     [sg.Push(), sg.Button('Guardar', key='-GUARDAR-', size=(10, 2))]]

        layout = [[sg.Column(left_col), sg.Column(right_col)]]

        # Creamos la ventana con el layout
        window = sg.Window('Etiquetar Imágenes', layout, size=(800, 600))
        self.window = window

    def convert_to_bytes(file_or_bytes, resize=None):
        if isinstance(file_or_bytes, str):
            img = PIL.Image.open(file_or_bytes)
        else:
            try:
                img = PIL.Image.open(io.BytesIO(
                    base64.b64decode(file_or_bytes)))
            except Exception as e:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = PIL.Image.open(dataBytesIO)

        cur_width, cur_height = img.size
        if resize:
            new_width, new_height = resize
            scale = min(new_height/cur_height, new_width/cur_width)
            img = img.resize(
                (int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

    def guardar_metadata(filename, tags, desc, perfil_actual):
        current_dir = os.path.abspath(__file__)

        relative_path = "datos/metadata.csv"
        ruta_metadata = os.path.join('./', relative_path)

        img = PIL.Image.open(filename)
        try:
            with open(ruta_metadata, mode='a', encoding='UTF-8') as file:
                csv_writer = csv.writer(file, lineterminator='\n')
                csv_writer.writerow([img.filename, desc, img.size, os.path.getsize(
                    filename), img.format, tags, perfil_actual, datetime.datetime.now()])
        except FileNotFoundError:
            with open(ruta_metadata, mode='w', encoding='UTF-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(
                    ['Ruta', 'Texto', 'Resolucion', 'Tamaño', 'Tipo', 'Tags', 'Perfil', 'Actualizacion'])
                csv_writer.writerow([img.filename, desc, img.size, os.path.getsize(
                    filename), img.format, tags, perfil_actual, datetime.datetime.now()])

    # --------------------------------- Event Loop ---------------------------------

    def iniciar_ventana(self):
        desc = ''
        tags = ''
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'AgregarTags':
                # Obtenemos los valores de los campos
                tags = values['-TAGS-']
                self.window.Element("-TAGVALUE-").Update(tags)
            if event == 'AgregarDesc':
                desc = values['-DESC-']
                self.window.Element("-DESCVALUE-").Update(desc)
            if event == 'Volver':
                # Cerramos la ventana
                self.window.close()
            if event == '-FOLDER-':
                folder = values['-FOLDER-']
                try:
                    file_list = os.listdir(folder)
                except:
                    file_list = []
                fnames = [f for f in file_list if os.path.isfile(
                    os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                self.window['-FILE LIST-'].update(fnames)
            elif event == '-FILE LIST-':
                try:
                    filename = os.path.join(
                        values['-FOLDER-'], values['-FILE LIST-'][0])
                    self.window['-TOUT-'].update(filename)
                    image_bytes = ventanaEtiquetar.convert_to_bytes(filename, resize=(400, 400))
                    self.window['-IMAGE-'].update(data=image_bytes)
                    img = PIL.Image.open(filename)
                    self.window['-TAMAÑO-'].update(os.path.getsize(filename))
                    self.window['-TIPO-'].update(img.format)
                    self.window['-RESOLUCION-'].update(img.size)
                except Exception as E:
                    print(f'* Error {E} *')
                    pass
            if event == '-GUARDAR-':
                ventanaEtiquetar.guardar_metadata(filename, tags, desc, 'perfil_actual')
                sg.popup_no_border('Se guardo correctamente la metadata de la imagen')
            elif event == 'volver':
                menu = menu_principal_ventana.VentanaMenu()
                menu.iniciar_ventana()

ventana= ventanaEtiquetar()
ventana.iniciar_ventana()