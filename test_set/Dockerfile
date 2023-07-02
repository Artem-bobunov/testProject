# Указываем базовый образ
FROM python:3.9

# Устанавливаем переменную среды для работы внутри контейнера
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем код проекта внутрь контейнера
COPY . /code/

# Определяем команду запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
