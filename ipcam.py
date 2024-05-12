import requests
from bs4 import BeautifulSoup
import pypyodbc as odbc

driver = 'Driver={ODBC Driver 17 for SQL Server};'
server = 'Server=localhost\SQLEXPRESS;Database=spts;Trusted_Connection=True;'
connection_string = "Driver={SQL Server};Server=localhost\\SQLEXPRESS;Database=spts;Trusted_Connection=yes;"

def save_to_database(camera_data):
    try:
        conn = odbc.connect(connection_string)
        cursor = conn.cursor()

        for name, url in camera_data:
            cursor.execute("INSERT INTO CameraBrands (Name, Url) VALUES (?, ?)", (name, url))

        conn.commit()
        print("Data saved successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

url = "https://zayifakim.com/uretici-ip-kamera-rtsp-url-listeleri.html"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    figure_tag = soup.find('figure', class_='wp-block-table')
    if figure_tag:
        table_tag = figure_tag.find('table')
        if table_tag:
            camera_data = []

            for tr_tag in table_tag.find_all('tr'):
                td_tags = tr_tag.find_all('td')

                if len(td_tags) >= 2:
                    name = td_tags[0].get_text(strip=True)
                    url = td_tags[1].get_text(strip=True)

                    camera_data.append((name, url))

            save_to_database(camera_data)
        else:
            print("No <table> tag found within <figure class='wp-block-table'>.")
    else:
        print("No <figure> tag with class 'wp-block-table' found.")
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
