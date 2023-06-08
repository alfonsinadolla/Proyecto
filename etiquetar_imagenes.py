import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64
import csv
import datetime
import menu_principal_ventana
import inicio_ventana

class ventanaEtiquetar:

    def __init__(self):
         """
           Inicializa la clase ventanaEtiquetar.

           Crea las columnas de la interfaz gráfica.
        """
         
         left_col = [[sg.Text('Bienvenido a Etiquetar Imagenes',font=('Arial', 12), background_color='white', text_color='black')],
                [sg.Text('Folder',background_color='white', text_color='black'), sg.In(size=(25,1),background_color='white', text_color='black', enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(button_color='black')],
                [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-', background_color='white', text_color= 'black')],
                [sg.Text('Tags',background_color='white', text_color='black')],
                [sg.Input(key='-TAGS-',background_color='white', text_color='black'), sg.Button('Agregar',button_color='black',key='AgregarTags')],
                [sg.Text('Descripción',background_color='white', text_color='black')],
                [sg.Input(key='-DESC-',background_color='white', text_color='black'), sg.Button('Agregar',button_color='black',key='AgregarDesc')]]

         right_col = [[sg.Button('Volver',button_color='black',size=(10,2),pad=((280,0),(0,0)))],
                        [sg.Text(size=(40,1),text_color='black',background_color='white', key='-TOUT-')],
                        [sg.Image(key='-IMAGE-', size=(340,340))],
                        [sg.Text('Tamaño:',background_color='white', text_color='black',key='-TAMAÑO-')],
                        [sg.Text('Tipo:',background_color='white', text_color='black',key='-TIPO-')],
                        [sg.Text('Resolucion:',background_color='white', text_color='black',key=('-RESOLUCION-'))],
                        [sg.Text("",background_color='white', text_color='black', key="-TAGVALUE-")],
                        [sg.Text("",background_color='white', text_color='black', key="-DESCVALUE-")],
                        [sg.Push(background_color='white'),sg.Button('Guardar',button_color='black',key='-GUARDAR-',size=(10,2))]]


         layout = [[sg.Column(left_col,background_color='white'), sg.Column(right_col,background_color='white')]]

         #Crea la ventana con el layout
         self.window = sg.Window('Etiquetar Imágenes', layout,size=(800,600),background_color='white')
         
    def convert_to_bytes(self,file_or_bytes, resize=None):
         
         """
        Convierte una imagen en bytes y, opcionalmente, cambia su tamaño.

        Args:
            file_or_bytes (str o bytes): Ruta de la imagen o bytes de la imagen.
            resize (tuple): Tamaño de la imagen resultante (ancho, alto).

        Devuelve la imagen convertida en bytes.
        """
         if isinstance(file_or_bytes, str):
            img = PIL.Image.open(file_or_bytes)
         else:
            try:
                img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
            except Exception as e:
                dataBytesIO = io.BytesIO(file_or_bytes)
                img = PIL.Image.open(dataBytesIO)

         cur_width, cur_height = img.size
         if resize:
            new_width, new_height = resize
            scale = min(new_height/cur_height, new_width/cur_width)
            img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
         bio = io.BytesIO()
         img.save(bio, format="PNG")
         del img
         return bio.getvalue()

    def imagen_existe(self,ruta_imagen, ruta_csv):
        """
        Verifica si la imagen ya existe en el archivo CSV.

        Args:
            ruta_imagen (str): Ruta de la imagen a verificar.
            ruta_csv (str): Ruta del archivo CSV.

        Devuelve True si la imagen existe en el archivo CSV o False en caso contrario.
        """
        with open(ruta_csv, mode= 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if ruta_imagen in row:
                    return True
        return False
    
    def guardar_metadata (self,filename,tags,desc,perfil_act,ruta_metadata):
        """
        Guarda la metadata de la imagen en el archivo CSV.

        Args:
            filename (str): Ruta de la imagen.
            tags (str): Etiquetas de la imagen.
            desc (str): Descripción de la imagen.
            perfil_act (str): Perfil actual.
            ruta_metadata (str): Ruta del archivo CSV.
        """
        img = PIL.Image.open(filename)
        try:
            with open (ruta_metadata,mode='a',encoding='UTF-8') as file:
                csv_writer=csv.writer(file,lineterminator='\n')
                csv_writer.writerow([img.filename,desc,img.size,os.path.getsize(filename), img.format,tags,perfil_act,datetime.datetime.now()])
        except FileNotFoundError:
            with open (ruta_metadata,mode='w',encoding='UTF-8') as file:
                csv_writer=csv.writer(file)
                csv_writer.writerow(['Ruta','Texto','Resolucion','Tamaño','Tipo','Tags','Perfil','Actualizacion'])
                csv_writer.writerow([img.filename,desc,img.size,os.path.getsize(filename), img.format,tags,perfil_act,datetime.datetime.now()])

    def editar_metadata(self, filename, tags, desc, perfil_act,ruta_metadata):
        """
        Edita una fila existente en el archivo CSV con la nueva información.

        Args:
            filename (str): Ruta de la imagen.
            tags (str): Etiquetas de la imagen.
            desc (str): Descripción de la imagen.
            perfil_act (str): Perfil actual.
            ruta_metadata (str): Ruta del archivo CSV.
        """

        img = PIL.Image.open(filename)
        #Lee el archivo CSV completo
        with open(ruta_metadata, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        #Busca la fila que deseamos editar, empieza en 1 para saltar la fila de encabezados
        for i in range(1, len(rows)): 
            if rows[i][0] == filename:
                #Reemplaza la fila completa con los nuevos valores
                rows[i] = [img.filename, desc, img.size, os.path.getsize(filename), img.format, tags, perfil_act, datetime.datetime.now()]
                break

        #Escribe todas las filas en un nuevo archivo CSV
        with open(ruta_metadata, mode='w', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def iniciar_ventana(self, perfil_act):
        desc=''
        tags=''
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'AgregarTags':
                '''Obtenemos los valores de los campos'''
                tags = values['-TAGS-']
                self.window.Element("-TAGVALUE-").Update(tags)
            if event == 'AgregarDesc':
                desc = values['-DESC-']
                self.window.Element("-DESCVALUE-").Update(desc)
            if event == 'Volver':
                self.window.close()
                menu = menu_principal_ventana.VentanaMenu(perfil_act)
                menu.iniciar_ventana()
            if event == '-FOLDER-':                        
                folder = values['-FOLDER-']
                try:
                    file_list = os.listdir(folder)         
                except:
                    file_list = []
                fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
                self.window['-FILE LIST-'].update(fnames)
            elif event == '-FILE LIST-':    
                try:
                    filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
                    self.window['-TOUT-'].update(filename)
                    image_bytes = self.convert_to_bytes(filename, resize=(340,340))
                    self.window['-IMAGE-'].update(data=image_bytes)
                    img = PIL.Image.open(filename)
                    self.window['-TAMAÑO-'].update(os.path.getsize(filename))
                    self.window['-TIPO-'].update(img.format)
                    self.window['-RESOLUCION-'].update(img.size)
                except Exception as E:
                    print(f'* Error {E} *')
                    pass       
            if event == '-GUARDAR-':
                current_dir = os.path.abspath(__file__) 
                relative_path = "datos/metadata.csv"
                ruta_metadata = os.path.join('./', relative_path)
                if self.imagen_existe(filename,ruta_metadata):
                    self.editar_metadata(filename,tags,desc,perfil_act,ruta_metadata)
                    with open('logs.csv', 'a', encoding ='UTF-8') as logs:
                        c = csv.writer(logs)
                        c.writerow([perfil_act,datetime.datetime.now(),'modifico una imagen previamente clasificada'])
                else:
                    self.guardar_metadata(filename,tags,desc,perfil_act,ruta_metadata)
                    with open('logs.csv', 'a', encoding ='UTF-8') as logs:
                        c = csv.writer(logs)
                        c.writerow([perfil_act,datetime.datetime.now(),'modifico una nueva imagen clasificada'])
                sg.popup_no_border('Se guardo correctamente la metadata de la imagen')
            elif event == 'volver' or event == sg.WIN_CLOSED:
                menu = menu_principal_ventana.VentanaMenu()
                menu.iniciar_ventana()
