from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        if User.objects.filter(username='admin', is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Database already seeded!'))
        else:
            User.objects.create_superuser(
                'admin', 'admin@example.com', 'admin'
            )
            self.stdout.write(self.style.SUCCESS('Database seeded!'))
