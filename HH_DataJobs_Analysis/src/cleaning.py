import numpy as np 
import pandas as pd 


class Cleaner():
    def __init__(self, config: dict):
        self.config = config 

    def __map_positions(self, data):
        filter_pos = self.config.get('role_filter')
        X = data_n = data[data['name'].str.contains(filter_pos, case=False, regex=True)].copy()

        return X

    def __map_level(self, data):
        X = data.copy()
        map_level = self.config.get('level_map')
        X['level'] = X['expirence'].map(map_level)

        return X

    def __map_currency(self, data):
        X = data.copy()
        map_currency = self.config.get('currency_map')

        X['salary_from_rub'] = X['salary_from'] * X['currency'].map(map_currency)
        X['salary_to_rub'] = X['salary_to'] * X['currency'].map(map_currency)
        
        return X

    def __clean_salary_from_to(self, data):
        X = data.copy()

        sfr_min = X.groupby('level')['salary_from_rub'].min().to_dict()
        str_min = X.groupby('level')['salary_to_rub'].min().to_dict()

        X['salary_from_rub'] = X['salary_from_rub'].fillna(X['level'].map(sfr_min))
        X['salary_to_rub'] = X['salary_to_rub'].fillna(X['level'].map(str_min))

        return X

    def clean(self, data):
        data = self.__map_positions(data)
        data = self.__map_level(data)
        data = self.__map_currency(data)
        data = self.__clean_salary_from_to(data)

        return data

    def run(self, inp: str, outp: str):
        data = pd.read_csv(inp)
        cleaned = self.clean(data)
        cleaned.to_csv(outp, index=False)

