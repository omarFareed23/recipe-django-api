"""
Django command to wait for the database to be available
"""
from typing import Any
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    "wait for the DB command"

    def handle(self, *args: Any, **options: Any) -> str:
        self.stdout.write('waiting for database...')
        cnt = 0
        dp_up = False
        while not dp_up and cnt < 50:
            try:
                self.check(databases=['default'])
                dp_up = True
            except (Psycopg2OperationalError, OperationalError) as e:
                self.stdout.write(str(e))
                cnt += 1
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        if dp_up:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(self.style.ERROR('Database unavailable!'))
