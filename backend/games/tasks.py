# games/tasks.py

from celery import shared_task
from django.core.management import call_command

@shared_task
def fetch_games_task():
    call_command('fetch_games')
