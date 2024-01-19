# импорт объекта для создания приложения
from flask import Flask, session

# создание экземпляра объекта приложения
app = Flask(__name__)
# app.run(debug=True)
# установим секретный ключ для подписи.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# здесь необходимо указать все контроллеры страниц
# закомментировать еще не реализованные
import controllers.index
import controllers.check