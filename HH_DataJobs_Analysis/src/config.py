
DIRTY_PATH = '/home/brs/ML-portfolio/HH_DataJobs_Analysis/data/parse_data.csv'
CLEAN_PATH = '/home/brs/ML-portfolio/HH_DataJobs_Analysis/data/clean_data.csv'

HEADERS = {
        'User-Agent' : 'MyCoolApp/1.0 (bursin04@bk.ru)'
        }

CONFIG = {
    'level_map' :  {
            'Нет опыта': 'Intern/Junior',
            'От 1 года до 3 лет': 'Junior/Middle',
            'От 3 до 6 лет': 'Middle/Senior',
            'Более 6 лет': 'Senior/Lead',},

    'currency_map' : {
            'RUB' : 1.0, 
            'USD': 90.0,
            'USD': 90.0,},
    'role_filter' : 'Аналитик|Analyst|Data|данных|science|scientist',
}
