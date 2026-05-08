import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.boxofficemojo.com/year/world/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")

data = []

for row in rows[1:]:
    cols = row.find_all("td")

    # Ensure row has expected structure
    if len(cols) >= 6:

        rank = cols[0].text.strip()

        # Movie title is inside a link (<a>)
        title_tag = cols[1].find("a")
        title = title_tag.text.strip() if title_tag else cols[1].text.strip()

        worldwide = cols[2].text.strip()
        domestic = cols[3].text.strip()
        foreign = cols[5].text.strip()

        data.append({
            "Rank": rank,
            "Title": title,
            "Worldwide Revenue": worldwide,
            "Domestic Revenue": domestic,
            "Foreign Revenue": foreign
        })

df = pd.DataFrame(data)

# Clean numeric columns
revenue_columns = [
    "Worldwide Revenue",
    "Domestic Revenue",
    "Foreign Revenue"
]

for col in revenue_columns:
    df[col] = (
        df[col]
        .replace(r'[\$,]', '', regex=True)
        .replace('-', '0')
    )

    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

df["Rank"] = pd.to_numeric(df["Rank"], errors='coerce').fillna(0).astype(int)

print(df.head(10))

df.to_csv("box_office_worldwide.csv", index=False)

print("\nSaved to box_office_worldwide.csv")