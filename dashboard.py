import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title='Employee KPI Dashboard', layout='wide')
engine = create_engine('sqlite:///employee_kpi.db')
data = pd.read_sql('SELECT * FROM kpi JOIN employees ON kpi.emp_id = employees.emp_id', engine)
data['review_date'] = pd.to_datetime(data['review_date'])

st.title('📊 Employee KPI Dashboard')

# Filters
department_list = ['All'] + sorted(data['department'].unique().tolist())
dept = st.selectbox('Department', department_list)

if dept != 'All':
    data = data[data['department'] == dept]

st.header('Average KPI by Department')
avg = data.groupby('department')[['sales','customer_satisfaction','tasks_completed']].mean().round(2)
st.dataframe(avg)

st.header('Top Employees by Customer Satisfaction')
top_csat = data.groupby('name')['customer_satisfaction'].mean().sort_values(ascending=False).head(10)
st.bar_chart(top_csat)

st.header('Productivity (tasks / hour)')
data['productivity'] = data['tasks_completed'] / data['hours_worked']
prod = data.groupby('name')['productivity'].mean().sort_values(ascending=False).head(20)
st.bar_chart(prod)
