import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

os.makedirs('outputs', exist_ok=True)
engine = create_engine('sqlite:///employee_kpi.db')

employees = pd.read_sql('SELECT * FROM employees', engine)
kpi = pd.read_sql('SELECT * FROM kpi', engine)
data = kpi.merge(employees, on='emp_id')
data['review_date'] = pd.to_datetime(data['review_date'])

print('Employees:', len(employees))
print('KPI rows:', len(kpi))

avg_dept = data.groupby('department')[['sales','customer_satisfaction','tasks_completed']].mean().round(2)
print('\nAverage KPI by department:\n', avg_dept)
avg_dept.to_csv('outputs/avg_kpi_by_department.csv')

top_csat = data.groupby('name')['customer_satisfaction'].mean().sort_values(ascending=False).head(10)
top_csat.to_csv('outputs/top_csat.csv')
print('\nTop 10 by csat:\n', top_csat)

prod = data.groupby('name').agg({'tasks_completed':'sum','hours_worked':'sum'})
prod['productivity'] = (prod['tasks_completed'] / prod['hours_worked']).round(3)
prod = prod.sort_values('productivity', ascending=False)
prod.to_csv('outputs/productivity.csv')
print('\nTop 10 by productivity:\n', prod.head(10))

plt.figure(figsize=(10,6))
prod['productivity'].head(20).plot(kind='bar')
plt.title('Top 20 Employee Productivity (tasks per hour)')
plt.ylabel('Tasks per hour')
plt.tight_layout()
plt.savefig('outputs/productivity.png')
plt.close()

plt.figure(figsize=(10,6))
avg_dept.plot(kind='bar')
plt.title('Average KPI by Department')
plt.ylabel('Value')
plt.tight_layout()
plt.savefig('outputs/avg_kpi_by_department.png')
plt.close()

print('\nSaved CSVs and PNGs to outputs/ directory.')
