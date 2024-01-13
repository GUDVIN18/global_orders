from flask import Flask
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from selenium import webdriver

chrome_driver_path = "/home/a0870221/domains/bot_global_orders/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# app = Flask(__name__)

# def update_google_sheet():


# # Инициализация драйвера
# driver = webdriver.Chrome()

# Открываем страницу входа
login_url = 'https://global.cdek.ru/login'
driver.get(login_url)

# Находим поле ввода email по CSS-селектору
email_field = driver.find_element(By.CSS_SELECTOR, 'input#inputEmail')
# Вводим ваш email
email_field.send_keys('egoe2002@gmail.com')

# Находим поле ввода пароля по CSS-селектору
password_field = driver.find_element(By.CSS_SELECTOR, 'input#inputPassword')
# Вводим ваш пароль
password_field.send_keys('Lalka1212')

password_field.send_keys(Keys.RETURN)

# Теперь вы находитесь в аккаунте и можете перейти на страницу, где нужно извлечь информацию
target_url = 'https://global.cdek.ru/office/outgoing'
driver.get(target_url)

# Найдем все элементы с классом "tracking" и "status"
tracking_elements = driver.find_elements(By.CLASS_NAME, 'tracking')
status_tracking_elements = driver.find_elements(By.CLASS_NAME, 'status.outgoing-sent')

# Создаем список для хранения данных
tracking_data = []

# Пройдемся по всем элементам и добавим их в список
for i in range(len(tracking_elements)):
    tracking = tracking_elements[i].text
    status = status_tracking_elements[i].text
    tracking_data.append({'Tracking': tracking, 'Status': status})

# Авторизуемся в Google Таблице с помощью ключа JSON
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Applications/prog/tgBot_Global_Orders/globalorders-a5541fea450a.json', scope)
client = gspread.authorize(creds)

# Открываем Google Таблицу по ее имени
spreadsheet = client.open('Orders Global Orders')  # Укажите имя своей таблицы

# Открываем лист в таблице
worksheet = spreadsheet.sheet1  # Если лист имеет другое имя, укажите его

# Получить текущие данные из таблицы, если они есть
try:
    existing_data = worksheet.get_all_values()
    if existing_data:
        df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
    else:
        df = pd.DataFrame(columns=['Tracking', 'Status'])
except gspread.exceptions.WorksheetNotFound:
    df = pd.DataFrame(columns=['Tracking', 'Status'])

# Перебираем данные, чтобы проверить, есть ли уже tracking в таблице
for data in tracking_data:
    tracking_value = data['Tracking']
    status_value = data['Status']

    if not df.empty and tracking_value in df['Tracking'].values:
        # Если найдено совпадение tracking, обновляем статус
        index = df[df['Tracking'] == tracking_value].index[0]
        df.at[index, 'Status'] = status_value
    else:
        # Если не найдено совпадение tracking, добавляем новую строку
        new_row = pd.DataFrame([[tracking_value, status_value]], columns=['Tracking', 'Status'])
        df = pd.concat([df, new_row], ignore_index=True)

# Очищаем лист перед обновлением данных
worksheet.clear()

# Записываем обновленные данные в таблицу
data = df.values.tolist()
header = df.columns.tolist()
data.insert(0, header)

worksheet.insert_rows(data, value_input_option='RAW')

# Закрываем браузер
url = 'https://docs.google.com/spreadsheets/d/1Z-HhuUd6q31rglaCzHPtunlR9jwqd3h2r_TY7EJQtXA/edit#gid=0'
driver.get(url)
time.sleep(5)
driver.quit()


# @app.route('/')
# def index():
#     update_google_sheet()
#     return 'Данные успешно обновлены в Google Таблице!'

# if __name__ == '__main__':
#     app.run(debug=True)
