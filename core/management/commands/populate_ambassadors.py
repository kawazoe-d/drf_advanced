from django.core.management import BaseCommand

from faker import Faker

from core.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(30):
            # create()は、入力されたデータから「保存用のオブジェクトを作成し、保存する」
            user = User.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='',
                is_ambassador=True
            )
            user.set_password('1234')
            # save()は、オブジェクトとして「保存する」（自力で保存用オブジェクトを作成する必要がある)
            user.save()