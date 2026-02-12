import requests
import json
import pandas as pd
import time 
import re



class HHParser():
    
    def __init__(self, headers):
        self.headers = headers
        self.all_ids = None
        self.all_vac = None
    
    def collect_vacancies_id(self, url: str = 'https://api.hh.ru/vacancies',
                      text: str = 'Data Analyst', # OR Аналитик данных OR BI analyst',
                      area: int = 1,
                      per_page: int = 50,
                      max_pages:int = 50):


        params = {
            'text' :  text,
            'area' : area,
            'per_page' : per_page,
            }


        all_ids = []
        for page in range(max_pages):
            params['page'] = page

            response=requests.get(url, params=params, headers=self.headers)

            if response.status_code != 200:
                print('СТАУС ОШИБКИ:', response.status_code)
                time.sleep(5)
                continue

            data = response.json()
            ids = [v.get('id') for v in data.get('items', [])]

            all_ids += ids
            time.sleep(0.3)

        print('Finish')
        self.all_ids = all_ids

    
    def parsing_by_id(self, urlc: str = 'https://api.hh.ru/vacancies'):
        
        '''
        params = {
            #'text' :  text,
            #'area' : area,
            'per_pages' : per_page,
            }
        '''
        
        all_items = []
        for idx in self.all_ids:

            url = f'{urlc}/{idx}'

            response = requests.get(url, headers=self.headers)

            if response.status_code!=200:
                print('СТАТУС ОБОСРАННЫХ ШТАНИШЕК:', response.status_code)
                time.sleep(5)
                continue

            vdata = response.json()
            all_items.append(vdata)
            
            time.sleep(0.3)

        print('Vac collected')
        self.all_vac = all_items
            


    def vacancies_to_csv(self, outp: str):

        def clear_description(data):
            return re.sub(r"<[^>]+>", "", data, flags=re.S)

        def get_empl_name(v):
            bt = v.get('employer')
            name = None

            if bt and len(bt) != 0:
                name = bt.get('name')

            return name

        def get_salary(v):
            salary = v.get('salary', None)
            s = False
            salary_from = None
            salary_to = None
            currency = None

            if salary:
                s = True 
                salary_from = salary.get('from')
                salary_to = salary.get('to')
                currency = salary.get('currency')

            return s, salary_from, salary_to, currency

        def get_prof_role(v):
            pr =  v.get('professional_roles')
            name = None 
            
            if pr:
                name = pr[0].get('name')

            return name 

        def get_exp(v):
            exp_arr = v.get('experience')
            exp = None 

            if exp_arr and len(exp_arr) != 0:
                exp = exp_arr.get('name')

            return exp

        def get_desc(v):
            desc = v.get('description')

            if desc:
                desc = clear_description(desc)

            return desc
        
        def get_skills(v):
            sk_arr = v.get('key_skills')

            if sk_arr:
                return [sk.get('name') for sk in sk_arr if sk.get('name')]

            return list()


        cols = ['id',
                'name',
                'city',
                'expirence',
                'empl_name',
                'desc',
                'salary',
                'salary_from',
                'salary_to',
                'currency',
                'key_skills',
                'test']

        df  = pd.DataFrame(columns=cols)

        for v in self.all_vac:
            idx = v.get('id', -1)
            name = get_prof_role(v) 
            area = v.get('area', {}).get('name', None)
            expirence = get_exp(v)
            desc = get_desc(v)
            employer = get_empl_name(v)
            is_salary, salary_from, salary_to, currency = get_salary(v)
            key_skills = get_skills(v)
            test = v.get('has_test', None)

            s = pd.DataFrame({
                'id' : [idx],
                'name' : [name],
                'city' : [area], 
                'desc' : [desc],
                'expirence' : [expirence],
                'empl_name' : [employer],
                'salary' : [is_salary],
                'salary_from' : [salary_from],
                'salary_to' : [salary_to],
                'currency' : [currency],
                'key_skills' : [key_skills],
                'test' : [test]
                })
            df = pd.concat([df, s], ignore_index=True)


        df['currency'] = df['currency'].replace({'RUR' : 'RUB'})
        df['key_skills_json'] = df['key_skills'].apply(json.dumps)
        df.to_csv(outp, index=False)


    def run(self, outp: str):
        self.collect_vacancies_id(max_pages=50)
        self.parsing_by_id()
        self.vacancies_to_csv(outp)




