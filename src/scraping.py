from pypdf import PdfReader

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import llm

edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option("detach", True)


class CVReader:
    def __init__(self, cv_path):
        self.reader = PdfReader(cv_path)
        self.driver = webdriver.Edge(options=edge_options)

    def read_pdf(self):
        """Classifies the data read from the user CV in PDF and generates a Data Frame"""

        text = ''

        for i, page in enumerate(self.reader.pages):
            text += page.extract_text()

        # TODO 1: Quizá haya que recategorizar las categorias para que no haya duplicados con distintos nombres,
        #  mediante otra llamada a OpenAI que identifique sinónimos

        return llm.classify(text)

    def read_linkedin(self):
        """Classifies the data read from the user LinkedIn profile."""

        self.driver.get("webpage")
        return


class WebScraper:

    def __init__(self):
        self.driver = webdriver.Edge(options=edge_options)

    def retrieve_offer_data(self, job_specs):
        """Retrieves the data from the offers and sends it to the classifier class.
        Additionally, if first run, generates an SQL database for future use cases.
        If not first run, compares with database and updates avoiding duplicates."""

        # TODO: Read job_specs and put it in the search bar in linkedin.

        print("HASTA AQUÍ HEMOS LLEGAO")

        self.driver.get("webpage")

        return

    def fill_application(self):
        """Scrapes application webs to fill in the CV data taken from your CV."""
        self.driver.get("webpage")

        search = self.driver.find_element(By.NAME, value="tagname")
        search.send_keys("TEXTODESEADO", Keys.ENTER)

        # TODO 2: Necesita un diccionario de posibles sinónimos para identificar correctamente los textos de las webs
        #  y rellenar acorde a ello. Se obtiene de OpenAI

        return
