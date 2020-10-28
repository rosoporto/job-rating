import requests
import logging


logging.basicConfig(level=logging.DEBUG)


def get_vacancies_hh(vacancy: str, area: int = 1, period: int = 30) -> list:
    page: int = 0
    vacancies: list = []
    params: dict = {'text': vacancy, 'area': area, 'period': period, 'per_page': 100, 'page': page}
    url: str = 'https://api.hh.ru/vacancies'
    response: requests.Response = requests.get(url, params=params, verify=True)
    response.raise_for_status()
    pages: int = response.json()['pages']
    while page < pages:
        params['page'] = page
        response = requests.get(url, params=params, verify=True)
        response.raise_for_status()
        vacancies.append(response.json())
        page += 1
    return vacancies


def predict_rub_salary(vacancie: dict) -> int:
    '''
    Salary forecast in rubles vacancies
    '''
    avg_salery = None
    job_salary = vacancie['salary']
    if job_salary is None or job_salary['currency'] != 'RUR':
        return avg_salery
    elif job_salary['from'] is None:
        avg_salery = int(job_salary['to'] * 0.8)         
    elif job_salary['to'] is None:
        avg_salery = int(job_salary['from'] * 1.2)
    else:
        avg_salery = int((job_salary['from'] + job_salary['to']) / 2)

    if avg_salery < 40000:
        return None
    return avg_salery
    

def get_statistics_salarys(programming_langs: list) -> dict:
    salary_statistics = {}
    for program_lang in programming_langs:
        vacancies_pages = get_vacancies_hh(program_lang)
        
        salarys = [predict_rub_salary(vacancy)
                    for vacancies_page in vacancies_pages
                    for vacancy in vacancies_page['items']
                    if predict_rub_salary(vacancy) is not None]        

        program_lang_statiс = {}
        program_lang_statiс['vacancies_found'] = vacancies_pages[-1]['found']
        program_lang_statiс['vacancies_processed'] = len(salarys)
        program_lang_statiс['average_salary'] = int(sum(salarys) / len(salarys))
        salary_statistics[program_lang] = program_lang_statiс

    return salary_statistics


def get_vacancies_sj(secret_key: str):
    headers = {'X-Api-App-Id': secret_key}
    params = {}
    url: str = 'https://api.superjob.ru/2.0/vacancies/'
    response: requests.Response = requests.get(url, headers=headers, params=params, verify=True)
    response.raise_for_status()
    print(response.json())