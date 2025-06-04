import re
import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Descargar recursos necesarios de NLTK (solo la primera vez)
nltk.download('punkt_tab')
nltk.download('stopwords')

# Nombre del archivo de salida
output_file_name = "clean_information.txt"

def clean_text(text):
    """
    Limpia el texto eliminando caracteres no deseados, pero conserva letras con tilde.
    """
    # Convertir a minúsculas
    text = text.lower()

    # Eliminar caracteres especiales (excepto letras, números, espacios, comas y letras con tilde)
    text = re.sub(r'[^a-z0-9 ,áéíóúüñ]', '', text)

    # Normalizar espacios (reemplazar múltiples espacios por uno solo)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def tokenize_text(text):
    """
    Tokeniza el texto en palabras individuales.
    """
    # Tokenización usando NLTK
    tokens = word_tokenize(text)

    # Eliminar stopwords (palabras comunes que no aportan significado)
    stop_words = set(stopwords.words('spanish'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

def process_file(file_path, output_file, offer_count):
    """
    Lee un archivo de texto, lo limpia y lo tokeniza, y guarda los tokens en un archivo.
    """
    try:
        # Leer el archivo de texto
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:

            text = file.read()

        # Limpieza del texto
        cleaned_text = clean_text(text)

        # Tokenización del texto
        tokens = tokenize_text(cleaned_text)

        # Escribir los tokens en el archivo de salida
        with open(output_file, 'a', encoding='utf-8') as output:
            output.write("=== Tokens ===\n")
            output.write(", ".join(tokens) + "\n\n")

        print(f"Los tokens de '{file_path}' se han guardado en '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Verificar que se hayan pasado argumentos
    if len(sys.argv) < 2:
        print("Uso: python script.py <archivo1> <archivo2> ...")
        sys.exit(1)

    # Obtener los nombres de los archivos desde argv
    input_files = sys.argv[1:]

    # Contar cuántas entradas son
    num_entries = len(input_files)
    print(f"Se procesarán {num_entries} archivos.")

    # Diccionario para manejar ofertas repetidas
    offer_counts = {}

    # Procesar cada archivo y guardar los resultados en el archivo de salida
    for file_path in input_files:
        # Obtener el nombre base del archivo (sin ruta)
        base_name = file_path.split('/')[-1]

        # Contar cuántas veces ha aparecido este nombre de oferta
        if base_name in offer_counts:
            offer_counts[base_name] += 1
        else:
            offer_counts[base_name] = 1

        # Procesar el archivo
        process_file(file_path, output_file_name, offer_counts[base_name])

    print(f"Todos los tokens se han guardado en '{output_file_name}'.")
