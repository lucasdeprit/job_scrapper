from playwright.sync_api import sync_playwright

def search_wwr_jobs(keywords: str) -> list[dict]:
    query = "+".join(keywords.lower().split())
    url = f"https://weworkremotely.com/remote-jobs/search?term={query}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, timeout=60000)

        # Esperar un poco más por si hay popups de cookies
        page.wait_for_timeout(5000)

        # Aceptar el popup de anuncios si está presente
        try:
            allow_all_button = page.query_selector("div#adroll_allow_all")
            if allow_all_button:
                allow_all_button.click()
                print("Anuncios permitidos.")
        except Exception as e:
            print(f"No se encontró el botón de permitir anuncios: {e}")

        # Esperar para asegurarse que la página cargue completamente
        page.wait_for_timeout(3000)

        # Intentar hacer clic en el botón de cookies
        try:
            # Buscar el botón de consentimiento de cookies
            consent_button = page.query_selector("button.fc-button.fc-cta-consent, button[data-accept-cookies='true']")
            if consent_button:
                consent_button.click()
                print("Consentimiento de cookies aceptado.")
            else:
                print("No se encontró el botón de consentimiento.")
        except Exception as e:
            print(f"No se pudo hacer clic en el botón de consentimiento: {e}")


        # Seleccionar los trabajos con el nuevo selector basado en la estructura del HTML
        job_elements = page.query_selector_all("li.new-listing-container")

        jobs = []
        for job in job_elements:
            try:
                # Extraer datos del listado de trabajo
                title_el = job.query_selector("h4.new-listing__header__title")
                company_el = job.query_selector("p.new-listing__company-name")
                location_el = job.query_selector("p.new-listing__company-headquarters")
                link_el = job.query_selector("a")
                date_el = job.query_selector("p.new-listing__header__icons__date")

                if not title_el or not company_el or not link_el:
                    continue

                # Extraer los valores
                title = title_el.inner_text().strip()
                company = company_el.inner_text().strip()
                location = location_el.inner_text().strip() if location_el else "Remote"
                link = f"https://weworkremotely.com{link_el.get_attribute('href')}"
                date = date_el.inner_text().strip() if date_el else "No date provided"

                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "link": link,
                    "date": date
                })
            except Exception as e:
                print(f"Error al procesar un trabajo: {e}")
                continue

        browser.close()
        return jobs

