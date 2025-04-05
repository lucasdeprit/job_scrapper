from scraper.remoteok_scraper import search_wwr_jobs

if __name__ == "__main__":
    keywords = input("¿Qué tipo de trabajo estás buscando? ")
    jobs = search_wwr_jobs(keywords)

    print(f"\n🔎 Resultados para: {keywords}\n")
    for i, job in enumerate(jobs[:10], 1):
        print(f"{i}. {job['title']} - {job['company']}")
        print(f"   {job['location']}")
        print(f"   🔗 {job['link']}\n")

