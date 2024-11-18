import requests
import pdfplumber
import fitz  # PyMuPDF
from datetime import datetime

def descargar_boe():
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = f"https://boe.es/boe/dias/2024/11/18/pdfs/BOE-S-2024-278.pdf"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            archivo = f"BOE-{hoy}.pdf"
            with open(archivo, "wb") as f:
                f.write(response.content)
            print(f"Boletín guardado como: {archivo}")
            return archivo
        else:
            print(f"No se encontró el BOE para la fecha: {hoy}")
    except Exception as e:
        print(f"Error al descargar el BOE: {e}")

def buscar_convocatorias(archivo, palabra_clave="convocatoria"):
    try:
        with pdfplumber.open(archivo) as pdf:
            resultados = []
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                texto = pagina.extract_text()
                if texto:
                    for num_parrafo, parrafo in enumerate(texto.split("\n"), start=1):
                        if palabra_clave.lower() in parrafo.lower():
                            resultados.append(
                                {
                                    "pagina": num_pagina,
                                    "parrafo": num_parrafo,
                                    "contenido": parrafo.strip(),
                                }
                            )
            if resultados:
                print(f"Se encontraron {len(resultados)} coincidencias para '{palabra_clave}':")
                for res in resultados:
                    print(f"- Página {res['pagina']}, párrafo {res['parrafo']}: {res['contenido']}")
            else:
                print(f"No se encontraron coincidencias para '{palabra_clave}'.")
    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")


archivo_boe = descargar_boe()
if archivo_boe:
    buscar_convocatorias(archivo_boe)
