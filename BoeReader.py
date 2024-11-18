import requests
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

def buscar_y_crear_enlaces(archivo, palabra_clave="convocatoria"):
    try:
        doc = fitz.open(archivo)
        resultados = []

        for num_pagina in range(len(doc)):
            pagina = doc[num_pagina]
            palabras = pagina.search_for(palabra_clave)  # Busca todas las coincidencias
            for palabra in palabras:
                # Crear un enlace de texto a la misma página
                # Ajuste en la creación del enlace para que no se use 'kind' ni parámetros incorrectos
                pagina.insert_link({
                    "rect": palabra,  # Rectángulo de la palabra encontrada
                    "uri": f"#page={num_pagina + 1}"  # Enlace interno a la misma página
                })
                resultados.append({"pagina": num_pagina + 1, "rect": palabra})

        if resultados:
            nuevo_archivo = archivo.replace(".pdf", "_con_enlaces.pdf")
            doc.save(nuevo_archivo, deflate=True)
            print(f"Se encontraron {len(resultados)} coincidencias y se guardaron enlaces en: {nuevo_archivo}")
        else:
            print(f"No se encontraron coincidencias para '{palabra_clave}' en el archivo.")
    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")


archivo_boe = descargar_boe()
if archivo_boe:
    buscar_y_crear_enlaces(archivo_boe)
