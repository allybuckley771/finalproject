import sqlite3
import pandas as pd

conn = sqlite3.connect('box_office_worldwide.db')
cursor = conn.cursor()
df = pd.read_csv('box_office_worldwide.csv')
df.to_sql('box_office', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
