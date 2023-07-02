from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class ReceiveTaskTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_receive_task_valid_data(self):
        response = self.client.post(reverse('receive_task'), {'number_task': 123, 'status': 'в обработке'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': 'Task received'})
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.numberTask, 123)
        self.assertEqual(task.status, 'в обработке')

    def test_receive_task_invalid_data(self):
        response = self.client.post(reverse('receive_task'), {'number_task': None, 'status': None})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid data'})
        self.assertEqual(Task.objects.count(), 0)

class ProcessTaskTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_process_task(self):
        task = Task.objects.create(numberTask=123, status='в обработке')
        response = self.client.post(reverse('process_task'), {'task_id': task.id})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['task_id'], task.id)
        self.assertEqual(response_data['status'], 'в обработке')
        self.assertEqual(response_data['execution_time'], '10 seconds')

    def test_process_task_invalid_id(self):
        response = self.client.post(reverse('process_task'), {'task_id': 999})
        self.assertEqual(response.status_code, 404)
