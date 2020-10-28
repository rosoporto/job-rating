import logging
import util

logging.basicConfig(level=logging.DEBUG)


def main():
  SECRET_KEY = 'v3.r.133117830.0ebd4574f45c7b18210322b970b218dd5e40a7e2.c8f4a632274176e8a08988358b1c1c84008b333a'

  programming_langs = ['C#',
                      'Go',
                      'C++',
                      'PHP',
                      'Ruby',
                      'Java',
                      'Scala',
                      'Swift',
                      'Python',
                      'TypeScript',
                      'JavaScript']
                      

  #print(util.get_statistics_salarys(programming_langs))

  util.get_vacancies_sj(SECRET_KEY)


if __name__ == '__main__':
  main()
