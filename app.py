from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Функция для инициализации базы данных
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()

# Функция для получения всех сообщений из базы данных
def get_all_feedback():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, message FROM feedback")
        return cursor.fetchall()

# Маршрут для отображения и обработки формы
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        
        # Сохранение данных в базу данных
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
            conn.commit()

        return redirect("/")  # Перенаправление на страницу с формой

    return render_template("index.html")

# Маршрут для получения всех сообщений через GET (AJAX)
@app.route("/get_feedback", methods=["GET"])
def get_feedback():
    feedbacks = get_all_feedback()  # Получаем все сообщения
    feedback_list = [{"name": name, "message": message} for name, message in feedbacks]
    return jsonify(feedback_list)  # Отправляем список сообщений в формате JSON

if __name__ == "__main__":
    init_db()  # Инициализация базы данных при запуске
    app.run(host="0.0.0.0", port=5000)
