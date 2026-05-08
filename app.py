from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="/workspaces/finalproject/static"), name="static")

@app.get("/")
def home(request: Request, q: Optional[str] = Query(None, description="Search query for movie titles"), sort_by: Optional[str] = Query(None, description="Sort by revenue column")):
    conn = sqlite3.connect('box_office_worldwide.db')
    cursor = conn.cursor()
    
    order_by = "Rank"
    if sort_by == 'worldwide':
        order_by = "`Worldwide Revenue` DESC"
    elif sort_by == 'domestic':
        order_by = "`Domestic Revenue` DESC"
    elif sort_by == 'foreign':
        order_by = "`Foreign Revenue` DESC"
    
    query = f"SELECT Rank, Title, `Worldwide Revenue`, `Domestic Revenue`, `Foreign Revenue` FROM box_office"
    if q:
        query += " WHERE Title LIKE ?"
        cursor.execute(query + f" ORDER BY {order_by}", ('%' + q + '%',))
    else:
        cursor.execute(query + f" ORDER BY {order_by}")
    
    movies = cursor.fetchall()
    conn.close()
    
    with open("/workspaces/finalproject/static/index.html", "r") as f:
        html = f.read()
    
    html = html.replace("{{ q }}", q or "")
    
    rows = ""
    for movie in movies:
        foreign = movie[4] if movie[4] else (movie[2] - movie[3] if movie[2] and movie[3] else 0)
        rows += f'                <tr>\n                    <td>{movie[0]}</td>\n                    <td>{movie[1]}</td>\n                    <td>{movie[2]}</td>\n                    <td>{movie[3]}</td>\n                    <td>{foreign}</td>\n                </tr>\n'
    
    html = html.replace('            <tbody>\n                {% for movie in movies %}\n                <tr>\n                    <td>{{ movie[0] }}</td>\n                    <td>{{ movie[1] }}</td>\n                    <td>{{ movie[2] }}</td>\n                    <td>{{ movie[3] }}</td>\n                    <td>{{ movie[4] }}</td>\n                </tr>\n                {% endfor %}\n            </tbody>', f'            <tbody>\n{rows}            </tbody>')
    
    return HTMLResponse(html)