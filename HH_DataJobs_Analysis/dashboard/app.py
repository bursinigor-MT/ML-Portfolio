import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import json


PATH = '/home/brs/ML-portfolio/HH_DataJobs_Analysis/data/clean_data.csv'
st.set_page_config(layout="wide")
plt.rcParams.update({'font.size' : 16})
sns.set_theme(palette='deep', style='whitegrid')


@st.cache_data
def read_data(path: str):
    data = pd.read_csv(path)
    data['key_skills'] = data['key_skills_json'].apply(json.loads)

    return data 


def plot_DB():

    data = read_data(PATH)

    col1, col2, col3 = st.columns(3)

    col1.metric('Общее количество вакансий: ', len(data))
    col2.metric('Общее количество работодателей: ', data['empl_name'].nunique())
    col3.metric('Общее количество необходимых навыков: ', data.explode('key_skills')['key_skills'].nunique())

    st.markdown('---')
    selected_lvl = st.selectbox('Группа', ['Intern/Junior', 'Junior/Middle', 'Middle/Senior', 'Senior/Lead'])
    st.markdown('---')
    
    left_col, right_col = st.columns(2)

    #Скиллы
    with left_col:
        selected_count_sk = st.slider('Количество навыков', 2,10,5)
        tmp_d = data.explode('key_skills')
        rez_data = tmp_d.groupby(['level', 'key_skills']).size().reset_index(name='count')

        level_data = rez_data[rez_data['level'] == selected_lvl]
        level_data = level_data.sort_values('count', ascending=False).head(selected_count_sk)

        fig, ax = plt.subplots(figsize=(20, 15))
        sns.barplot(x=level_data['key_skills'], y=level_data['count'], ax=ax)
        ax.set_ylabel('Количество')
        ax.set_xlabel('Навыки')

        st.pyplot(fig)

    #Работодатели
    with right_col:
        selected_count_emp = st.slider('Количество работодателей', 2,10,5)
        data_empl = data['empl_name'].value_counts().reset_index(name='count').sort_values('count', ascending=False).head(selected_count_emp)

        fig, ax = plt.subplots(figsize=(20, 15))
        sns.barplot(x=data_empl['empl_name'], y=data_empl['count'], ax=ax)
        ax.set_ylabel('Количество')
        ax.set_xlabel('Работодатели')

        st.pyplot(fig)

    st.markdown('---')

    col1, col2 = st.columns(2)

    with col1:
        selected_lvl = st.selectbox('Группа', ['Intern/Junior', 'Junior/Middle', 'Middle/Senior', 'Senior/Lead', 'All'])
        if selected_lvl == 'All':
            data_lvl = data
        else:
            data_lvl = data[data['level'] == selected_lvl]

        pie_data = data_lvl['salary'].value_counts(dropna=False)
        pie_data = pie_data.rename(index={False:'Зарплата не указана', True : 'Зарплата указана'})
        labels = [f'{i} : {pie_data[i]}' for i in pie_data.index]

        fig, ax = plt.subplots(figsize=(10,10))
        wedges, texts, autotexts = ax.pie(pie_data, labels=None, autopct='%1.1f%%')
        ax.legend(wedges, labels, title='Категории и их количество')

        ax.set_title(f'Доля вакансий с указанной зарплатой в группе {selected_lvl}')        

        st.pyplot(fig)

    with col2:
        selected_lvl = st.selectbox('Группа', ['All'])
        pie_data_lvl = data['level'].value_counts()

        fig, ax = plt.subplots(figsize=(10,10))
        ax.pie(pie_data_lvl, labels=pie_data_lvl.index, autopct='%1.1f%%')
        ax.set_title('Доля вакансий по уровню соискателя')        

        st.pyplot(fig)





plot_DB()

