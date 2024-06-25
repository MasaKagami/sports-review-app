# games/management/commands/fetch_games.py

import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from games.models import Game
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Fetch games from API-Football and update the database'

    def handle(self, *args, **kwargs):
        api_key = settings.API_FOOTBALL_KEY
        url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'
        headers = {
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }

        response = requests.get(url, headers=headers)
        self.stdout.write(self.style.SUCCESS(f"Status Code: {response.status_code}"))
        self.stdout.write(self.style.SUCCESS(f"API Response: {response.json()}"))

        data = response.json()

        if 'response' not in data:
            self.stdout.write(self.style.ERROR("Key 'response' not found in the API response"))
            return

        for item in data['response']:
            game_data = item['fixture']
            teams_data = item['teams']
            goals_data = item['goals']

            game, created = Game.objects.update_or_create(
                slug=slugify(f"{game_data['league']['name']}-{teams_data['home']['name']}-{teams_data['away']['name']}"),
                defaults={
                    'title': game_data['status']['long'],
                    'date': game_data['date'],
                    'team1': teams_data['home']['name'],
                    'team2': teams_data['away']['name'],
                    'score_team1': goals_data['home'] if goals_data['home'] is not None else 0,
                    'score_team2': goals_data['away'] if goals_data['away'] is not None else 0,
                    'tournament': game_data['league']['name'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Game {game.title} created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Game {game.title} updated'))
