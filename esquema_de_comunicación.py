pip install PyPDF2

import random
from PyPDF2 import PdfReader

# Componente 1: Fuente de Información (Leer el archivo PDF)
def leer_archivo_pdf(archivo_pdf):
    pdf_reader = PdfReader(archivo_pdf)
    texto = ''
    for page in pdf_reader.pages:
        texto += page.extract_text()
    return texto

archivo_pdf = "Peter Pan.pdf"

mensaje_original = leer_archivo_pdf(archivo_pdf)

# Componente 2: Transmisor (Codificación a binario)
def codificar_a_binario(datos):
    return ''.join(format(ord(char), '08b') for char in datos)

datos_binarios = codificar_a_binario(mensaje_original)

# Componente 3: Canal (Simulación de ruido)
def simular_ruido(datos_binarios, probabilidad_error=0.1):
    datos_con_ruido = ''
    for bit in datos_binarios:
        if random.random() < probabilidad_error:
            # Cambiar el bit si se cumple la probabilidad de error
            datos_con_ruido += '1' if bit == '0' else '0'
        else:
            datos_con_ruido += bit
    return datos_con_ruido

datos_con_ruido = simular_ruido(datos_binarios, probabilidad_error=0.2)

# Componente 4: Receptor (Decodificación desde binario)
def decodificar_desde_binario(datos_binarios):
    return ''.join(chr(int(datos_binarios[i:i+8], 2)) for i in range(0, len(datos_binarios), 8))

mensaje_recibido = decodificar_desde_binario(datos_con_ruido)

# Componente 5: Destino de Información
print("Mensaje original (desde el archivo PDF): ", mensaje_original)
print("Mensaje recibido (con ruido y decodificado): ", mensaje_recibido)
