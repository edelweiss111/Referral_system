import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone=os.getenv('PHONE'),
            first_name='Admin',
            last_name='Admin1',
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('DATABASE_PASSWORD'))
        user.save()
