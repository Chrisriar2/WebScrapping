from playwright.sync_api import sync_playwright

file_name = "information_CCO.txt"

with sync_playwright() as playwright:
    # Launch the browser
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)  # slow_mo is in milliseconds
    # Create a new page
    page = browser.new_page()
    # Visit the page
    page.goto("https://www.occ.com.mx/empleos/de-diseñador-gráfico/en-ciudad-de-mexico/")

    # Locate all elements with an ID starting with "jobcard-"
    jobcard_elements = page.locator('[id^="jobcard-"]')

    # Get the count of elements
    count = jobcard_elements.count()
    print(f"Found {count} job cards.")

    target = open(file_name,"w")
    target.truncate()

    
    # Loop through pages 
    for i in range (6):
        # Loop through each element and click it
        for j in range(count):
            # Get the specific element by index
            jobcard = jobcard_elements.nth(j)
            # Wait for the element to be visible
            jobcard.wait_for(state="visible", timeout=30000)

            jobcard.click()

            #title_element = jobcard.locator('p[class*="text-"]')
            #title_element.wait_for(state="visible", timeout=30000)
            #title = title_element.inner_text()
            #print(f"Job Card {i + 1} Title: {title}")

            #print(f"Clicked job card {i + 1}.")

            #wait for the job details to be visible 
            #job_detail_container = page.locator('#job-detail-containter')
            #job_detail_container.wait_for(state="visible",timeout=30000)

            #job_detail_text 
            job_details_div = page.locator("#job-detail-container")
            
            job_details_div.wait_for(state="visible",timeout=30000)

            #Locating the title
            title_element = job_details_div.locator("p.text-\\[24px\\].leading-\\[110\\%\\]")
           
            salary_element = job_details_div.locator("p.text-\\[18px\\].leading-6")
        
            description_elemnts = job_details_div.locator("div.flex.flex-col.gap-2")

            details_elemnt = job_details_div.locator('div[class*="flex"][class*="mb-1"]')

            more_elemnt = job_details_div.locator("div.break-words.mb-8")

            title_text = title_element.inner_text()

            salary_text = salary_element.inner_text()

            description_text = description_elemnts.inner_text()

            details_text = details_elemnt.inner_text()

            more_text = more_elemnt.inner_text()

            target.write(f">> Job card {j+1} ")
            target.write(f"Job Title: {title_text}\n")
            target.write(f"Salary : {salary_text}\n")
            target.write(f"About: \n {description_text}\n")
            target.write(f"Details: \n {details_text}\n")
            target.write(f"More: \n {more_text}\n")
            

            #description_text = description_elemnts.inne = job_detail_container.locator('p.')  CHECK THIS

            # Optional: Add a delay or navigate back if needed
            page.wait_for_timeout(1000)  # Add a delay if necessary
            # page.go_back()  # Navigate back if the click opens a new page
        page.locator("li.rounded-\\[6px\\]").nth(1).click()

    # Close the browser
    browser.close()
    target.close()
