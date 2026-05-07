
import time
from client import APIClient

endpoint = "https://www.themuse.com/api/public/jobs"

class JobExtractor:

    def __init__(self, page_qty, data):
        self.page_qty = page_qty
        self.data = data
        self.apiclient = APIClient(endpoint)

        self.total_pages = 0
        self.total_vacancies = 0
        self.logs = []

    def logger(self):

        self.status_code = self.apiclient.get_status_code()
        try:
            status = None
            if self.status_code == 200:
                status = "Sucess"
            else:
                status = "Failed"

            log = {
                "status_code": self.status_code,
                "actual_page": self.get['page'],
                "total_per_page": len(self.get['results']),
                "status": status,
                "total_vacancies": self.total_vacancies
            }
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        else:
            return log

    def data_pagination(self):
        """ método que itera por pela quantidade de páginas definidas """
        job_vacancy = []
        for page in range(1, self.page_qty +1):
            #loop que faz a paginação
            self.data['page'] = page
            time.sleep(1.5)
            self.get = self.apiclient.metodo_get(self.data)
            self.total_pages +=1
            self.logs.append(self.logger())
            for result in self.get['results']:
                self.total_vacancies +=1
                job_vacancy.append(result)
        return job_vacancy