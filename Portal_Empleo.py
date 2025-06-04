from playwright.sync_api import sync_playwright

file_name = "information_PDE.txt"

with sync_playwright() as playwright:
    # Launch the browser
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()

    # Navigate to the target page
    page.goto("https://www.empleo.gob.mx/PortalDigital")

    # Wait for the page to fully load
    page.wait_for_load_state("networkidle")

    # Prompt the user to manually fill in the fields and solve the CAPTCHA
    print("Please fill in the required fields and solve the CAPTCHA in the browser window.")
    input("Press Enter after completing the form and solving the CAPTCHA...")

    # Debugging: Print all button elements with the class
    button_elements = page.query_selector_all('button.btn.btn-gold.px19.align-center.mt-3.btn-xl')

    target = open(file_name,"w")
    target.truncate()

    # Click the "Buscar" button
    try:
        page.click('button.btn.btn-gold.px19.align-center.mt-3.btn-xl')
        print("Button clicked successfully.")
    except Exception as e:
        print(f"Failed to click button: {e}")

    # Wait for the job listings to load
    page.wait_for_timeout(10000)

    # Locate all div elements with the class 'backItemList'
    jobcard_elements = page.locator('div.backItemList')

    # Count the number of elements found
    count = jobcard_elements.count()

    # Iterate through each job card
    for i in range(count):
        jobcard = jobcard_elements.nth(i)

        # Wait for the job card to be visible
        jobcard.wait_for(state="visible", timeout=30000)

        # Click the job card
        jobcard.click()

        # Locate the "Ver oferta" button within the current job card
        try:
            see_ofert_button = jobcard.locator('a.btnPrimary.btn-lg[href*="/puesto-de-trabajo/vacante/"]')
            see_ofert_button.click()
            print(f"Clicked 'Ver oferta' button for job card {i + 1}.")
        except Exception as e:
            print(f"Failed to click 'Ver oferta' button for job card {i + 1}: {e}")

        # Wait for 5 seconds after clicking "Ver oferta"
        page.wait_for_timeout(5000)

        # Extract the job title
        try:
            # Refine the locator to target only the job title
            job_title_element = page.locator('div.col-md-7 h2.montserrat-regular.px28').nth(0)
            place_element = page.locator('div.col-md-7 h3.montserrat-extraLight').nth(1) 
            company = page.locator('div.col-md-7 h3.montserrat-extraLight').nth(2) 
            salary_element = page.locator('div.col-md-4 h2.montserrat-regular.mb-4.px28')
            job_description_element = page.locator('div.col-7 p.montserrat-light.px16').first
            requirements_list = page.locator('ul:has(li.montserrat-light.px16)')
            requirements_items = requirements_list.locator('li.montserrat-light.px16').all_inner_texts()
            #EXTRAER EL NOMBRE DE LA EMPRESA 

            job_title = job_title_element.inner_text()
            place_job = place_element.inner_text()
            company_name = company.inner_text()
            salary = salary_element.inner_text()
            job_description = job_description_element.inner_text()
            requirements_text = "\n".join(requirements_items)

            target.write(f">> Job card {i+1}")
            target.write(f"Job title: {job_title}")
            target.write(f"Job place:{place_job}")
            target.write(f"Company name: {company_name}")
            target.write(f"Salary: {salary}")
            target.write(f"Job description: {job_description}")
            target.write(f"Requirements:\n{requirements_text}")
            target.write("\n")

        except Exception as e:
            print(f"Failed to extract information for job card {i + 1}: {e}")

        # Locate the "Regresar a resultados" button
        try:
            back_button = page.locator('a.nav-link.active').filter(has=page.locator('img[alt="star"]'))
            back_button.wait_for(state="visible", timeout=1000)
            back_button.click()
            print(f"Clicked 'Regresar a resultados' button for job card {i + 1}.")
        except Exception as e:
            print(f"Failed to click 'Regresar a resultados' button for job card {i + 1}: {e}")

        # Wait for the job listings to reload
        page.wait_for_timeout(500)

    # Close the browser
    browser.close()
