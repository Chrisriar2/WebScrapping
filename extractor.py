import re
import mysql.connector
import spacy

# Cargar el modelo de lenguaje de spaCy para español
nlp = spacy.load("es_core_news_sm")

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "web_scrapping"
}

# Función para conectarse a MySQL
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Función para crear la tabla si no existe
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_offers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            salario TEXT,
            ubicacion TEXT,
            habilidades TEXT,
            idiomas TEXT,
            educacion TEXT,
            software TEXT,
            jornada TEXT,
            modalidad TEXT,
            estado TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Funciones de extracción
def extract_salary(text):
    salary_pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:semanal|quincenal|mensual|anual)'
    return ", ".join(re.findall(salary_pattern, text))

def extract_location(text):
    doc = nlp(text)
    return ", ".join([ent.text for ent in doc.ents if ent.label_ == "LOC"])

def extract_soft_skills(text):
    keywords = ["trabajo en equipo", "comunicación", "liderazgo", "proactividad", "adaptabilidad"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_software(text):
    keywords = ["adobe", "photoshop", "illustrator", "figma", "after effects", "premiere"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_languages(text):
    keywords = ["inglés", "español", "francés", "alemán"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_education(text):
    keywords = ["universitario", "licenciatura", "titulado", "diplomado", "maestría"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_work_schedule(text):
    keywords = ["tiempo completo", "medio tiempo", "jornada parcial"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_modality(text):
    keywords = ["presencial", "remoto", "híbrido"]
    return ", ".join([kw for kw in keywords if kw in text])

def extract_job_status(text):
    keywords = ["activa", "cerrada", "en proceso"]
    return ", ".join([kw for kw in keywords if kw in text])

# Función para procesar y almacenar los datos en MySQL
def process_and_store_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    job_cards = re.split(r'Job, title', text, flags=re.IGNORECASE)
    job_cards = [card.strip() for card in job_cards if card.strip()]

    conn = connect_db()
    cursor = conn.cursor()

    for card in job_cards:
        salario = extract_salary(card)
        ubicacion = extract_location(card)
        habilidades = extract_soft_skills(card)
        idiomas = extract_languages(card)
        educacion = extract_education(card)
        software = extract_software(card)
        jornada = extract_work_schedule(card)
        modalidad = extract_modality(card)
        estado = extract_job_status(card)

        cursor.execute("""
            INSERT INTO job_offers (salario, ubicacion, habilidades, idiomas, educacion, software, jornada, modalidad, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (salario, ubicacion, habilidades, idiomas, educacion, software, jornada, modalidad, estado))

    conn.commit()
    cursor.close()
    conn.close()
    print("Datos insertados en la base de datos correctamente.")

# Crear la tabla antes de insertar datos
create_table()

# Procesar el archivo y almacenar datos en MySQL
input_file = "clean_information.txt"
process_and_store_file(input_file)
