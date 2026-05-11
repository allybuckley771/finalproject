from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Session, select, create_engine

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

app = FastAPI()
app.mount("/static", StaticFiles(directory="/workspaces/finalproject/static"), name="static")

@app.get("/")
def home(request: Request, q: str | None = Query(None, description="Search query for movie titles"), sort_by: str | None = Query(None, description="Sort by revenue column")):
    query = select(BoxOffice)
    if q:
        query = query.where(BoxOffice.title.contains(q))

    if sort_by == 'worldwide':
        query = query.order_by(BoxOffice.worldwide_revenue.desc())
    elif sort_by == 'domestic':
        query = query.order_by(BoxOffice.domestic_revenue.desc())
    elif sort_by == 'foreign':
        query = query.order_by(BoxOffice.foreign_revenue.desc())

    with Session(engine) as session:
        movies = session.exec(query).all()

    with open("/workspaces/finalproject/static/index.html", "r") as f:
        html = f.read()

    html = html.replace("{{ q }}", q or "")

    rows = ""
    for movie in movies:
        foreign = movie.foreign_revenue if movie.foreign_revenue else (movie.worldwide_revenue - movie.domestic_revenue if movie.worldwide_revenue and movie.domestic_revenue else 0)
        rows += f'                <tr>\n                    <td>{movie.rank}</td>\n                    <td>{movie.title}</td>\n                    <td>{movie.worldwide_revenue}</td>\n                    <td>{movie.domestic_revenue}</td>\n                    <td>{foreign}</td>\n                </tr>\n'

    html = html.replace('            <tbody>\n                {% for movie in movies %}\n                <tr>\n                    <td>{{ movie[0] }}</td>\n                    <td>{{ movie[1] }}</td>\n                    <td>{{ movie[2] }}</td>\n                    <td>{{ movie[3] }}</td>\n                    <td>{{ movie[4] }}</td>\n                </tr>\n                {% endfor %}\n            </tbody>', f'            <tbody>\n{rows}            </tbody>')

    return HTMLResponse(html)
