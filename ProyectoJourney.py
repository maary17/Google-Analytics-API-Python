from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from tkinter import Tk, Label,  Text, Button, Frame, messagebox, filedialog, ttk, Scrollbar, VERTICAL, HORIZONTAL
import gspread
import tkinter  as tk
import pandas as pd
from gspread_dataframe import set_with_dataframe
from tkcalendar import Calendar
from tkcalendar import Calendar, DateEntry

creds = Credentials.from_service_account_file('api-python-380220-366fd91b39ae.json')

analytics = build('analyticsreporting', 'v4', credentials=creds)

"""
CONEXION A GOOGLE SHEETS
"""
gc = gspread.service_account(filename='googlesheets.json')
sh_prueba = gc.open('Journey').sheet1
sh_prueba.clear()


def reporte_GA(lista, limite, fecha_inf, fecha_sup):
    global DF_FINAL
    DF_FINAL = pd.DataFrame(columns=['userID', 'URL', 'Pageviews'])
    columnas_DF=DF_FINAL.columns.tolist()
    columnas_CRUCE=['userID']
    if check_canal.get() == 1:
        columnas_DF.append('Default Channel Grouping (Canales predeterminados)')
        columnas_CRUCE.append('Default Channel Grouping (Canales predeterminados)')
    if check_genero.get() == 1:
        columnas_DF.append('Genero Contratante')
        columnas_CRUCE.append('Genero Contratante')
    if check_edad.get() == 1:
        columnas_DF.append('Edad Contratante')
        columnas_DF.append('Rango edad')
        columnas_CRUCE.append('Edad Contratante')
        columnas_CRUCE.append('Rango edad')

    CRUCE = BD_USERID_SD[columnas_CRUCE]
    DF_FINAL = pd.DataFrame(columns=columnas_DF)
    print(DF_FINAL)

    global sh_prueba
    sh_prueba.clear()

    IDS=[]
    if limite==-1:
        IDS=lista
    else:
        IDS = lista[:limite]

    sh_prueba.insert_row(columnas_DF, 1)
    for userID in IDS:
        report = analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': '242748645',
                        'dateRanges': [{'startDate': fecha_inf, 'endDate': fecha_sup}],
                        'metrics': [{'expression': 'ga:pageviews'}],
                        'dimensions': [{'name': 'ga:pagePath'}],
                        'dimensionFilterClauses': [
                            {
                                'filters': [
                                    {
                                        'dimensionName': 'ga:dimension3',  # Nombre de la dimensión personalizada
                                        'expressions': [userID],  # Valor a comparar
                                        'operator': 'EXACT'  # Operador de comparación
                                    }
                                ]
                            }
                        ]
                    }]
            }
        ).execute()
        data = []
        reports = report.get('reports', [])
        data = [{'userID': userID, 'URL': row['dimensions'][0], 'Pageviews': row['metrics'][0]['values'][0]}
                for report in reports
                for row in report.get('data', {}).get('rows', [])]

        df = pd.DataFrame(data)
        if df.empty==False:
            print("DF: ", df)
            edad = check_edad.get()
            genero = check_genero.get()
            canal = check_canal.get()

            if edad==1 or genero==1 or canal==1:
              df=pd.merge(df, CRUCE, left_on='userID', right_on='userID', how='left')

            DF_FINAL = pd.concat([DF_FINAL, df], ignore_index=True)
            print(df)
            last_row = len(sh_prueba.get_all_values())
            sh_prueba.insert_rows(df.values.tolist(), row=last_row + 1)
            DF_FINAL.to_excel("sadjhajsha.xlsx")
        else:
            print("============= DF NO EXISTE ================")

BD_USERID = pd.read_excel('UserID.xlsx')
BD_USERID_SD=BD_USERID.drop_duplicates(['userID'], keep='last')


color_fondo='#01ced1'
ventana = Tk()
ventana.config(bg='white')
ventana.geometry('400x300')
ventana.minsize(width=500, height=300)
ventana.title('Google Analytics Automatización')
style = ttk.Style()
style.theme_use('default')
style.map('TCombobox', fieldbackground=[('readonly', 'white')])
style.map('TCombobox', selectbackground=[('readonly', 'white')])
style.map('TCombobox', selectforeground=[('readonly', 'black')])
#style.configure('TCheckbutton', background='white')
style.configure('TCheckbutton',
                background='white',   # color de fondo
                foreground='#000000',   # color del texto
                font=('Arial', 8),     # tamaño y tipo de fuente
                anchor='w',             # posición del marcador
                borderwidth=1,
                activeBackground='white',
                activeforeground='#000000',
                relief='flat'# oculta el marcador
                )


font1 = ('Calibri', 12, 'normal')
lista_desplegable_MES = ttk.Combobox(ventana, width=25, height=35, font=font1, justify='left')
lista_desplegable_MES['values'] = ['ENERO', 'FEBRERO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
lista_desplegable_MES['state'] = 'readonly'
lista_desplegable_MES.current(0)
lista_desplegable_MES.place(x=20, y=10)
altura=1
ancho=20

def buttonObtener():
    lista_ID=[]
    paginas=0
    print(lista_desplegable_MES.get())

    meses = {
        'ENERO': 1,
        'FEBRERO': 2,
        'SEPTIEMBRE': 9,
        'OCTUBRE': 10,
        'NOVIEMBRE': 11,
        'DICIEMBRE': 12
    }

    mes_seleccionado = lista_desplegable_MES.get()
    if mes_seleccionado in meses:
        mes_num = meses[mes_seleccionado]
        print(mes_num)
        print(mes_seleccionado)
        lista_ID = BD_USERID[BD_USERID['Mes Venta'] == mes_num]['userID'].unique().tolist()
    else:
        print('Mes no válido')

    paginas = {
        '5': 5,
        '10': 10,
        '50': 50,
        '100': 100,
        'TODOS': -1
    }
    pag_seleccionadas = lista_desplegable_Pag.get()
    print(pag_seleccionadas)
    if pag_seleccionadas in paginas:
        paginas = paginas[pag_seleccionadas]
        print("paginas", paginas)

    else:
        # Si la selección de páginas no está en el diccionario, podrías manejar el error aquí
        print('Número de páginas no válido')

    print(texto_inf.get())
    fecha_inf=texto_inf.get()
    fecha_sup = texto_sup.get()
    reporte_GA(lista_ID, paginas, fecha_inf, fecha_sup)
    #print(lista_ID[:5])
    messagebox.showinfo(message="Base de datos subida correctamente", title="Aviso")

def busqueda():

    print(entry.get())
    lista=[]


    fecha_inf = texto_inf.get()
    fecha_sup = texto_sup.get()
    print(fecha_inf)
    print(fecha_sup)
    lista.append(entry.get())
    reporte_GA(lista, 1, fecha_inf, fecha_sup)


boton1 = Button(ventana, text='Obtener', bg=color_fondo, font=('Arial', 8, 'bold'),
                fg='white', activebackground='white', command=buttonObtener, width=ancho, height = altura)
boton1.place(x=250, y=10)

entry = ttk.Entry(width=35, font=('Arial', 8, 'bold'))
entry.place(height=24, x=20, y=70)


boton1 = Button(ventana, text='Buscar', bg=color_fondo, font=('Arial', 8, 'bold'),
fg='white', activebackground='white',command=busqueda, width=ancho, height = altura)
boton1.place(x=250, y=70)

texto_inf=tk.StringVar()
rango_inf = DateEntry(ventana, width= 15, background= color_fondo, foreground="white", bd=2, textvariable=texto_inf, date_pattern='YYYY-MM-dd')
rango_inf.place(x=20, y=42)

texto_sup=tk.StringVar()
rango_sup = DateEntry(ventana, width= 15, background= color_fondo, foreground="white", bd=2, textvariable=texto_sup, date_pattern='YYYY-MM-dd')
rango_sup.place(x=130, y=42)

lista_desplegable_Pag = ttk.Combobox(ventana, width=22, height=35, font=('Arial', 8, 'normal'), justify='left')
lista_desplegable_Pag['values'] = ['5','10',  '50', '100', 'TODOS']
lista_desplegable_Pag['state'] = 'readonly'
lista_desplegable_Pag.current(0)
lista_desplegable_Pag.place(x=250, y=42)
check_edad = tk.IntVar()
checkbox_edad = ttk.Checkbutton(ventana, text="Edad", variable=check_edad)
checkbox_edad.place(x=20, y=100)

check_genero = tk.IntVar()
checkbox_genero = ttk.Checkbutton(ventana, text="Genero", variable=check_genero)
checkbox_genero.place(x=100, y=100)


check_canal = tk.IntVar()
checkbox_canal = ttk.Checkbutton(ventana, text="Canal", variable=check_canal)
checkbox_canal.place(x=200, y=100)



ventana.mainloop()