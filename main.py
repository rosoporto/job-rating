import os
import logging
import util
from dotenv import load_dotenv


logging.basicConfig(level=logging.DEBUG)


def main():
  load_dotenv()
  SECRET_KEY_SJ = os.getenv('SECRET_KEY_SJ')

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

  stat_hh = util.get_statistics_salarys_hh(programming_langs)
  stat_sj = util.get_statistics_salarys_sj(programming_langs, SECRET_KEY_SJ)

  util.rendering_statiс_data(stat_hh, 'HeadHunter')
  util.rendering_statiс_data(stat_sj, 'SuperJob')


if __name__ == '__main__':
  main()
