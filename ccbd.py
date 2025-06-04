from playwright.sync_api import sync_playwright
import mysql.connector

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Cambia si tienes contraseña
    "database": "web_scrapping"
}

def insertar_en_db(titulo, empresa, ubicacion, tiempo, salario, contrato, jornada, modalidad, detalles, requisitos):
    """Inserta los datos en la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        
        query = """INSERT INTO ofertas (titulo, empresa, ubicacion, tiempo, salario, contrato, jornada, modalidad, detalles, requisitos) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (titulo, empresa, ubicacion, tiempo, salario, contrato, jornada, modalidad, detalles, requisitos)

        cursor.execute(query, values)
        conexion.commit()
        print(f"✅ Oferta insertada correctamente: {titulo}")

    except mysql.connector.Error as e:
        print(f"❌ Error al insertar en la base de datos: {e}")

    finally:
        cursor.close()
        conexion.close()


def extraer_ofertas():
    """Ejecuta el scraping y almacena los datos en MySQL."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        page.goto("https://mx.computrabajo.com/empleos-de-diseno-artes-graficas-en-quintana-roo")

        for i in range(3):  # Recorrer las tarjetas de empleo
            jobcard_elements = page.locator("article.box_offer")
            count = jobcard_elements.count()
            print(f"🔍 Encontradas {count} ofertas de empleo")

            for j in range(count):
                jobcard = jobcard_elements.nth(j)
                jobcard.wait_for(state="visible", timeout=30000)
                jobcard.click()

                try:
                    job_details_div = page.locator('div.box_detail').first
                    job_details_div.wait_for(state="visible", timeout=30000)
                except Exception as e:
                    print(f"⚠️ No se pudo acceder a los detalles de la oferta: {e}")
                    continue

                try:
                    # Extraer los detalles del empleo
                    title_element = job_details_div.locator("p.title_offer.fs21.fwB.lh1_2")
                    company_element = job_details_div.locator("a.dIB.mr10")
                    place_element = job_details_div.locator("p.fs16.mb5").first
                    job_details_element = job_details_div.locator("div.mbB")
                    job_requirements_ul = job_details_div.locator("ul.fs16.disc.mbB")
                    time_element = job_details_div.locator("p.fc_aux.fs13").first

                    # Obtener los textos
                    title_text = title_element.inner_text()
                    company_text = company_element.inner_text()
                    place_text = place_element.inner_text()
                    time_text = time_element.inner_text() if time_element.count() > 0 else "No disponible"

                    # Extraer detalles adicionales del trabajo
                    job_details_text = [p.inner_text().strip() for p in job_details_element.locator("p").all()]

                    # Separar detalles (salario, contrato, jornada y modalidad)
                    salario = job_details_text[0] if len(job_details_text) > 0 else "No especificado"
                    contrato = job_details_text[1] if len(job_details_text) > 1 else "No especificado"
                    jornada = job_details_text[2] if len(job_details_text) > 2 else "No especificado"
                    modalidad = job_details_text[3] if len(job_details_text) > 3 else "No especificado"

                    # Resto de detalles
                    more_job_details = "\n".join(job_details_text[4:]) if len(job_details_text) > 4 else "No disponible"

                    # Extraer requisitos en viñetas
                    bullet_points = job_requirements_ul.locator("li").all_inner_texts()
                    requisitos_text = "\n".join(bullet_points)

                    # Insertar en la base de datos
                    insertar_en_db(title_text, company_text, place_text, time_text, salario, contrato, jornada, modalidad, more_job_details, requisitos_text)

                except Exception as e:
                    print(f"❌ Error al extraer información: {e}")

        browser.close()


if __name__ == "__main__":
    extraer_ofertas()
