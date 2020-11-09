import requests
import logging
from terminaltables import AsciiTable


logging.basicConfig(level=logging.DEBUG)


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif not salary_from:
        return int(salary_to * 0.8)
    elif not salary_to:
        return int(salary_from * 1.2)
    else:
        return None


def get_vacancies_hh(vacancy, area=1, period=30):
    page = 0
    vacancies = []
    params = {'text': vacancy, 'area': area, 'period': period, 'per_page': 100, 'page': page}
    url = 'https://api.hh.ru/vacancies'

    try:
        response = requests.get(url, params=params, verify=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    pages: int = response.json()['pages']
    while page < pages:
        params['page'] = page
        try:
            response = requests.get(url, params=params, verify=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        vacancies.append(response.json())
        page += 1
    return vacancies


def predict_rub_salary_hh(vacancie):
    job_salary = vacancie['salary']
    if job_salary is None or job_salary['currency'] != 'RUR':
        return None
    return predict_salary(job_salary['from'], job_salary['to'])
    

def get_statistics_salarys_hh(programming_langs):
    salary_statistics = {}
    for program_lang in programming_langs:
        vacancies_pages = get_vacancies_hh(program_lang)
        
        salarys = [predict_rub_salary_hh(vacancy)
                    for vacancies_page in vacancies_pages
                    for vacancy in vacancies_page['items']
                    if predict_rub_salary_hh(vacancy) is not None]        

        program_lang_statiс = {}
        program_lang_statiс['vacancies_found'] = vacancies_pages[-1]['found']
        program_lang_statiс['vacancies_processed'] = len(salarys)
        program_lang_statiс['average_salary'] = int(sum(salarys) / len(salarys))
        salary_statistics[program_lang] = program_lang_statiс

    return salary_statistics


def get_vacancies_sj(vacancy, secret_key):
    is_last_page = True
    page = 0
    vacancies = []
    headers = {'X-Api-App-Id': secret_key}
    params = {
        'town': 4,  # Moscow
        'period': 30,  # Last month
        'catalogues': 48,  # Development, Programming
        'keyword': vacancy, # Name of vacancy
        'no_agreement': 1, #Ignore vacancies without stated salary
        'page': page, #Job search start page
        'count': 100 #Number of results per request
    }
    url = 'https://api.superjob.ru/2.0/vacancies/'
    while is_last_page:
        try:
            response = requests.get(url,
                                    headers=headers,
                                    params=params,
                                    verify=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        vacancies.append(response.json())
        is_last_page = response.json()['more']
        page += 1
    return vacancies


def predict_rub_salary_sj(vacancy):
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']
    salary_vacancy = True if salary_from or salary_to else False

    if not salary_vacancy or vacancy['currency'] != 'rub':
        return None
    return predict_salary(salary_from, salary_to)


def get_statistics_salarys_sj(programming_langs, secret_key):
    salary_statistics = {}
    for program_lang in programming_langs:
        vacancies_pages = get_vacancies_sj(
                f'программист {program_lang}', secret_key)
        
        salarys = [predict_rub_salary_sj(vacancy)
                    for vacancies_page in vacancies_pages
                    for vacancy in vacancies_page['objects']
                    if predict_rub_salary_sj(vacancy) is not None]        
        
        program_lang_statiс = {}
        program_lang_statiс['vacancies_found'] = vacancies_pages[-1]['total']
        program_lang_statiс['vacancies_processed'] = len(salarys)
        program_lang_statiс['average_salary'] = int(sum(salarys) / (len(salarys) or 1))
        salary_statistics[program_lang] = program_lang_statiс

    return salary_statistics


def preparing_data_for_rendering(site_salary_stat):
    table_data = [
        ['Язык программирования',
        'Вакансий найдено',
        'Вакансий обработанно',
        'Средняя зарплата'],
    ]
    for lang, stats in site_salary_stat.items():
        statistics = []
        statistics.append(lang)
        for stat in stats.values():
            statistics.append(stat)
        table_data.append(statistics)
    return table_data


def rendering_statiс_data(statiс_data_on_vacancies, table_name):
    processed_data = preparing_data_for_rendering(statiс_data_on_vacancies)    
    print(AsciiTable(processed_data, table_name).table)

