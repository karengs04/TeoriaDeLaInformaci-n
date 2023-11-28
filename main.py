import random
import hashlib
from collections import Counter
import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
import heapq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def build_huffman_tree(message):
    # Calcula la frecuencia de cada símbolo en el mensaje
    symbol_freq = Counter(message)

    heap = [[weight, [char, ""]] for char, weight in symbol_freq.items()]
    heapq.heapify(heap)

    # Construye el árbol de Huffman
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_encode(message, huffman_tree):
    encoded_message = ""
    for char in message:
        for pair in huffman_tree:
            if char == pair[0]:
                encoded_message += pair[1]
                break
    return encoded_message

def huffman_decode(encoded_message, huffman_tree):
    decoded_message = ""
    current_bits = ""
    for bit in encoded_message:
        current_bits += bit
        for pair in huffman_tree:
            if current_bits == pair[1]:
                decoded_message += pair[0]
                current_bits = ""
                break
    return decoded_message

def build_shannon_fano_tree(message):
    def divide(nodes):
        if len(nodes) <= 1:
            return nodes
        mid = len(nodes) // 2
        for node in nodes[:mid]:
            node[1] += "0"
        for node in nodes[mid:]:
            node[1] += "1"
        return divide(nodes[:mid]) + divide(nodes[mid:])

    symbol_freq = {}
    for char in message:
        if char in symbol_freq:
            symbol_freq[char] += 1
        else:
            symbol_freq[char] = 1

    nodes = [[char, ""] for char in symbol_freq.keys()]
    sorted_nodes = sorted(nodes, key=lambda x: symbol_freq[x[0]], reverse=True)
    shannon_fano_tree = divide(sorted_nodes)

    return sorted(shannon_fano_tree, key=lambda x: x[0])

def shannon_fano_encode(message, shannon_fano_tree):
    if shannon_fano_tree is None:
        return message  # Devuelve la parte sin codificar si el árbol es None
    encoded_message = ""
    for char in message:
        for pair in shannon_fano_tree:
            if char == pair[0]:
                encoded_message += pair[1]
                break
    return encoded_message

def shannon_fano_decode(encoded_message, shannon_fano_tree):
    if shannon_fano_tree is None:
        return encoded_message  # Devuelve el mensaje codificado si el árbol es None
    decoded_message = ""
    current_bits = ""
    for bit in encoded_message:
        current_bits += bit
        for pair in shannon_fano_tree:
            if current_bits == pair[1]:
                decoded_message += pair[0]
                current_bits = ""
                break
    return decoded_message

def run_length_encode(message):
    # Implementa la codificación Run-Length
    encoded_message = ""
    char_count = 1
    for i in range(1, len(message)):
        if message[i] == message[i - 1]:
            char_count += 1
        else:
            encoded_message += message[i - 1] + str(char_count)
            char_count = 1
    encoded_message += message[-1] + str(char_count)
    return encoded_message

def run_length_decode(encoded_message):
    # Implementa la decodificación Run-Length
    decoded_message = ""
    i = 0
    while i < len(encoded_message):
        char = encoded_message[i]
        i += 1
        count = ""
        while i < len(encoded_message) and encoded_message[i].isdigit():
            count += encoded_message[i]
            i += 1
        decoded_message += char * int(count)
    return decoded_message

def simulate_packet_reception(encoded_message, selected_channel):
    noise_probability = 0.2  # 20% de probabilidad de ruido

    # Comprobar si se aplica ruido
    if random.random() < noise_probability:
        print(f"Canal {selected_channel + 1}: ¡Ruido detectado en la parte {selected_channel + 1}!")
        return None  # Simula una parte dañada

    return encoded_message

def substitution_encode(message, key):
    if key is None:
        return message
    encoded_message = ""
    for char in message:
        if char in key:
            encoded_message += key[char]
        else:
            encoded_message += char
    return encoded_message

def substitution_decode(encoded_message, key):
    if key is None:
        return "Error: Key is missing or None"

    decoded_message = ""
    if key:
        reverse_key = {v: k for k, v in key.items()}
        i = 0
        while i < len(encoded_message):
            char = encoded_message[i]
            i += 1
            count = ""
            while i < len(encoded_message) and encoded_message[i].isdigit():
                count += encoded_message[i]
                i += 1
            if char in reverse_key:
                decoded_message += reverse_key[char] * int(count)
            else:
                decoded_message += char * int(count)
    return decoded_message


def transmisor_single_part(part, method, tree_or_key):
    if method == "Huffman":
        if tree_or_key is None:
            print("No se puede codificar en Huffman sin un árbol Huffman. Asegúrate de seleccionar Huffman en el transmisor.")
            return None
        return huffman_encode(part, tree_or_key)
    elif method == "Shannon-Fano":
        return shannon_fano_encode(part, tree_or_key)
    elif method == "Run-Length":
        return run_length_encode(part)
    elif method == "Substitution":
        key = input("Ingrese la clave de sustitución (ejemplo: a->X, b->Y): ")
        key = dict(pair.split("->") for pair in key.split(", "))
        encoded_message = substitution_encode(part, key)  # Cambio pdf_text por part
        return encoded_message, key
    else:
        print("Método de codificación no válido.")
        return None

def receptor_single_part(encoded_message, method, tree_or_key):
    if method == "Huffman":
        return huffman_decode(encoded_message, tree_or_key)
    elif method == "Shannon-Fano":
        return shannon_fano_decode(encoded_message, tree_or_key)
    elif method == "Run-Length":
        return run_length_decode(encoded_message)
    elif method == "Substitution":
        return substitution_decode(encoded_message, tree_or_key)
    else:
        print("Método de decodificación no válido.")
        return None

def calculate_hash(message):
    return hashlib.sha256(message.encode()).hexdigest()

def find_hash(received_hash, sent_hashes):
    keys = list(sent_hashes.keys())
    keys.sort()  # Ordena las claves para realizar la búsqueda binaria
    left, right = 0, len(keys) - 1

    while left <= right:
        mid = (left + right) // 2
        if keys[mid] == received_hash:
            return keys[mid], sent_hashes[keys[mid]]
        elif keys[mid] < received_hash:
            left = mid + 1
        else:
            right = mid - 1

    return None, None


def main():
    pdf_file_path = "C:/Users/yamil/Desktop/Teoría de la Información/Entropia/Rapunzel.pdf"
    num_channels = 6
    num_parts = 6
    current_channel = 0
    damaged_part = None  # Inicialización de la variable
    damaged_channel = None  # Inicialización de la variable

    choice = input(
        "Seleccione el método de codificación (1 para Huffman, 2 para Shannon-Fano, 3 para Run-Length, 4 para Cifrado por Sustitución Simple): ")

    if choice == "1":
        method = "Huffman"
    elif choice == "2":
        method = "Shannon-Fano"
    elif choice == "3":
        method = "Run-Length"
    elif choice == "4":
        method = "Substitution"
    else:
        print("Opción no válida. Seleccione 1, 2, 3 o 4 para el método de codificación.")
        return

    pdf_reader = PyPDF2.PdfReader(pdf_file_path)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    print("Mensaje original:")

    if method == "Huffman":
        huffman_tree = build_huffman_tree(text)
    else:
        huffman_tree = None

    part_length = len(text) // num_parts
    parts = [text[i:i + part_length] for i in range(0, len(text), part_length)]

    sent_hashes = {}
    received_parts = [None] * num_parts  # Inicializamos received_parts

    while any(part is None for part in received_parts):
        part_idx = current_channel % num_parts
        encoded_message = transmisor_single_part(parts[part_idx], method, huffman_tree)

        if encoded_message is not None:
            sent_hash = calculate_hash(encoded_message)
            sent_hashes[sent_hash] = parts[part_idx]

            print(f"Parte {part_idx + 1} enviada por el canal {current_channel + 1}")
            received_part = simulate_packet_reception(encoded_message, current_channel)

            if received_part is not None:
                received_parts[part_idx] = received_part
            else:
                damaged_part = f"parte {part_idx + 1}"
                print(f"Ruido en el Canal {current_channel + 1}, {damaged_part} dañada, reenvío de parte")

                reconstructed_text = "".join(
                    received_part if received_part is not None else "" for received_part in received_parts)
                received_hash = calculate_hash(reconstructed_text)

                matching_hash, original_part = find_hash(received_hash, sent_hashes)

                if matching_hash is not None:
                    print("Mensaje recibido correctamente.")
                    print(f"Mensaje original para el hash {matching_hash}:")
                    print(original_part)
                else:
                    print("Ningún mensaje recibido coincide con el original.")
                    print("Sent hashes:")
                    print(sent_hashes)
                    print("Received hash not found in sent hashes.")

                current_channel = (current_channel + 1) % num_channels

    reconstructed_text = "".join(received_part if received_part is not None else "" for received_part in received_parts)

    decoded_message = receptor_single_part(reconstructed_text, method, huffman_tree)

    if decoded_message is not None:
        print("Mensaje decodificado:")
        print(decoded_message)

        pdf_writer = PdfWriter()

        c = canvas.Canvas("temp.pdf", pagesize=letter)
        c.drawString(100, 100, decoded_message)
        c.showPage()
        c.save()

        with open("temp.pdf", "rb") as temp_file:
            page = PdfReader(temp_file).pages[0]
            pdf_writer.add_page(page)

        print("Mensaje decodificado guardado como 'temp.pdf'")


if __name__ == "__main__":
    main()