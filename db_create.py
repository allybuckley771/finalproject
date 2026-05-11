import pandas as pd
from sqlmodel import SQLModel, Field, create_engine

class BoxOffice(SQLModel, table=True):
    __tablename__ = "box_office"

    rank: int | None = Field(default=None, primary_key=True)
    title: str
    worldwide_revenue: float
    domestic_revenue: float
    foreign_revenue: float

DB_NAME = "box_office_worldwide.db"
engine = create_engine(f"sqlite:///{DB_NAME}")
SQLModel.metadata.create_all(engine)

df = pd.read_csv('box_office_worldwide.csv')
df.columns = [c.lower().replace(' ', '_') for c in df.columns]
df.to_sql('box_office', engine, if_exists='replace', index=False)
