from flask import Flask, render_template
import psycopg2
from config import host, user, password, db_name

connection = psycopg2.connect(
    host = host,
    user = user,
    password = password,
    database = db_name,
)
connection.autocommit = True
cursor = connection.cursor()

cursor.execute("SELECT * FROM news")
news_data = cursor.fetchall()
connection.close()
print(news_data)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html', news=news_data)

@app.route('/politic')
def politic():
    return render_template('politic.html')

@app.route('/sport')
def sport():
    return render_template('sport.html')

@app.route('/science')
def scince():
    return render_template('science.html')


if __name__ == '__main__':
    app.run(debug=True)




