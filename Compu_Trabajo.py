from playwright.sync_api import sync_playwright

file_name = "information_CT.txt"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://mx.computrabajo.com/empleos-de-diseno-artes-graficas-en-puebla")

    # Abrir el archivo para escritura
    with open(file_name, "w", encoding="utf-8") as file:
        for i in range(3):  # Recorrer las tarjetas de empleo
            jobcard_elements = page.locator("article.box_offer")
            count = jobcard_elements.count()
            print(f"Found {count} job cards")

            for j in range(count):
                jobcard = jobcard_elements.nth(j)
                jobcard.wait_for(state="visible", timeout=30000)
                print(f"Job card offer: {j + 1} \n")
                jobcard.click()

                try:
                    job_details_div = page.locator('div.box_detail').first
                    job_details_div.wait_for(state="visible", timeout=30000)
                except Exception as e:
                    print(f"Failed to find box detail: {e}")
                    continue  # Saltar a la siguiente tarjeta si los detalles no se encuentran

                try:
                    # Extraer los detalles del empleo
                    title_element = job_details_div.locator("p.title_offer.fs21.fwB.lh1_2")
                    company_element = job_details_div.locator("a.dIB.mr10")
                    place_element = job_details_div.locator("p.fs16.mb5").first
                    job_details_element = job_details_div.locator("div.mbB")
                    job_requirements_ul = job_details_div.locator("ul.fs16.disc.mbB")
                    time_element = job_details_div.locator("p.fc_aux.fs13").first  # Nuevo

                    # Obtener los textos
                    title_text = title_element.inner_text()
                    company_text = company_element.inner_text()
                    place_text = place_element.inner_text()
                    time_text = time_element.inner_text() if time_element.count() > 0 else "No disponible"

                    # Extraer detalles adicionales del trabajo
                    job_details_text = [p.inner_text().strip() for p in job_details_element.locator("p").all()]
                    more_job_details = "\n".join(job_details_text)

                    # Extraer requisitos en viñetas
                    bullet_points = job_requirements_ul.locator("li").all_inner_texts()

                    # Imprimir resultados en la terminal
                    #print(f">> Job Title: {title_text}")
                    #print(f">> Company name: {company_text}")
                    #print(f">> Place: {place_text}")
                    #print(f">> Time: {time_text}")  # Nuevo
                    #print(f">> Details: {more_job_details}")
                    #print(f">> Requirements: {bullet_points}")
                    #print("-" * 50)

                    # Escribir en el archivo
                    file.write(f"Job Title: {title_text}\n")
                    file.write(f"Company Name: {company_text}\n")
                    file.write(f"Place: {place_text}\n")
                    file.write(f"Time: {time_text}\n")  # Nuevo
                    file.write(f"Details: {more_job_details}\n")
                    file.write("Requirements:\n")
                    for req in bullet_points:
                        file.write(f"- {req}\n")
                    file.write("-" * 50 + "\n")

                except Exception as e:
                    print(f"Something failed while getting information: {e}")

    browser.close()
