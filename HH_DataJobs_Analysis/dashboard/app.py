import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import json

st.set_page_config(layout="wide", page_title="HH.ru")

PATH = '/home/brs/ML-portfolio/HH_DataJobs_Analysis/data/clean_data.csv'
plt.rcParams.update({'font.size' : 16})


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
    
    with st.sidebar:
        st.title('Фильтры')
        selected_lvl = st.selectbox('Группа', ['Intern/Junior', 'Junior/Middle', 'Middle/Senior', 'Senior/Lead', 'All'])
        selected_count_sk = st.slider('Количество навыков', 2,10,5)
        selected_count_emp = st.slider('Количество работодателей', 2,10,5)

    
    tab_skills, tab_empl, tab_ratios = st.tabs(['Навыки', 'Работодатели', 'Обзор рынка'])
    
    with tab_skills: 
        left_col, right_col = st.columns([2,1])

        tmp_d = data.explode('key_skills')
        rez_data = tmp_d.groupby(['level', 'key_skills']).size().reset_index(name='count')
        if selected_lvl == 'All':
            level_data = rez_data 
        else:
            level_data = rez_data[rez_data['level'] == selected_lvl]
        level_data = level_data.sort_values('count', ascending=False).head(selected_count_sk)

     

        #Скиллы
        with left_col:
            ps_skills = px.bar(level_data, x='count', y='key_skills',
                               color='count',
                               color_continuous_scale='Viridis',
                               orientation='h')

            ps_skills.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(ps_skills, use_container_width=True)

        with right_col:
            tree_data = level_data.copy()
            tree_data['parent'] = 'Все навыки'


            ps_tree = px.treemap(tree_data, path=['parent','key_skills'], values='count',
                                 color='count',
                                 color_continuous_scale='Viridis',)
            st.plotly_chart(ps_tree)

    with tab_empl:
        #Работодатели
        data_empl = None
        if selected_lvl == 'All':
            level_data = data 
        else:
            level_data = data[data['level'] == selected_lvl]

        data_empl = level_data['empl_name'].value_counts().reset_index(name='count').sort_values('count', ascending=False).head(selected_count_emp)

        ps_empl = px.bar(data_empl, x='count', y='empl_name',
                         orientation='h',
                         color='count',
                        color_continuous_scale='Viridis')

        ps_empl.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(ps_empl)

    
    with tab_ratios:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Доля указания зарплаты')
            if selected_lvl == 'All':
                data_lvl = data
            else:
                data_lvl = data[data['level'] == selected_lvl]

            pie_data = data_lvl['salary'].value_counts(dropna=False)
            pie_data = pie_data.rename(index={False:'Зарплата не указана', True : 'Зарплата указана'}).reset_index()
            pie_data.columns = ['it_is', 'count']

            ps_salary = px.pie(pie_data, values='count', names='it_is', hole=0.4)
            
            st.plotly_chart(ps_salary, use_container_width=True)


        with col2:
            st.subheader("Распределение по грейдам")

            pie_data_lvl = data['level'].value_counts().reset_index()
            pie_data_lvl.columns = ['level', 'count']
            ps_group_levels = px.pie(pie_data_lvl, values='count', names='level',
                                     hole=0.4)
                                    
            st.plotly_chart(ps_group_levels, use_container_width=True)





plot_DB()

