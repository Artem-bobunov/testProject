from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegistrationForm, ReceiveTaskForm, ProcessTaskForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
import pika
from .models import Task
import time


# Create your views here.
def task(request):
    users = User.objects.all()
    return render(request, 'list.html', {'users': users})

# NeD1SNj2
# 2MsN18Gj


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def receive_task(request):
    """
        Функция receive_task отвечает за получение задачи
        и ее сохранение в базе данных, а также отправку
        задачи в очередь RabbitMQ
     """
    form = ReceiveTaskForm()  # Инициализация формы до условия

    if request.method == 'POST':
        # Инициализация формы с данными из POST-запроса
        form = ReceiveTaskForm(request.POST)
        # Проверка валидности данных в форме
        if form.is_valid():
            # Извлечение номера задачи из формы
            number_task = form.cleaned_data['number_task']
            # Извлечение статуса задачи из формы
            status = form.cleaned_data['status']
            if not number_task or not status:
                # Возврат ошибки в формате JSON, если данные некорректны
                return JsonResponse({'error': 'Invalid data'}, status=400)
            # Создание экземпляра модели Task и сохранение в базе данных
            task = Task.objects.create(numberTask=number_task, status=status)
            # Установление соединения с RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            # Объявление очередей для задач и ответов
            channel.queue_declare(queue='task_queue', durable=True)
            channel.queue_declare(queue='response_queue', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key='task_queue',
                body=str(task.id),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Делаем сообщения персистентными
                )
            )
            # Закрытие соединения с RabbitMQ
            connection.close()
            # Возврат успешного ответа в формате JSON
            return JsonResponse({'success': 'Task received'})
    # Отображение шаблона receive_task.html с передачей формы в контекст шаблона
    return render(request, 'receive_task.html', {'form': form})


def process_task(request):
    """Функция process_task отвечает за обработку задачи и отправку ответа."""
    form = ProcessTaskForm()

    if request.method == 'POST':
        form = ProcessTaskForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            task = get_object_or_404(Task, id=task_id)
            # Имитация обработки задачи (задержка на 10 секунд)
            time.sleep(10)
            # Изменение статуса задачи на "в обработке"
            task.status = 'в обработке'
            task.save()
            response_data = {
                'task_id': task.id,
                'status': task.status,
                'execution_time': '10 seconds',
            }
            # Установление соединения с RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.basic_publish(
                exchange='',
                routing_key='response_queue',
                body=str(response_data),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            connection.close()
            return JsonResponse(response_data)

    return render(request, 'process_task.html', {'form': form})
