from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 標準出力に上書きして表示する
        self.stdout.write('Waiting for the database...')
        conn = None

        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting for 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))