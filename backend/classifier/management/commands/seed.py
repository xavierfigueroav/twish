from django.contrib.auth.models import User
from django.core.management import BaseCommand

from ...models import App
from ...models import PredictionLabel
from ...models import Predictor


class Command(BaseCommand):

    def seed_user(self):
        if User.objects.filter(username='admin', is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('User table already seeded!'))
        else:
            User.objects.create_superuser(
                'admin', 'admin@example.com', 'admin'
            )
            self.stdout.write(self.style.SUCCESS('User table seeded!'))

    def seed_predictor(self):
        if Predictor.objects.exists():
            self.stdout.write(
                self.style.SUCCESS('Predictor table already seeded!')
            )
        else:
            predictor = Predictor.objects.create(
                name='LogisticRegression', version='v1.0',
                description='Example predictor LogisticRegression.'
            )
            for i in range(3):
                PredictionLabel.objects.create(
                    label=f'Label {i}', integer_label=i, predictor=predictor,
                    description=f'This is the example label {i}'
                )
            self.stdout.write(self.style.SUCCESS('Predictor table seeded!'))

    def seed_app(self):
        if App.objects.exists():
            self.stdout.write(self.style.SUCCESS('App table already seeded!'))
        else:
            predictor = Predictor.objects.get()
            App.objects.create(
                name='Example App',
                description='This is a Twish example app',
                about='This is a Twish example app. Etiam in condimentum justo, nec vehicula est. Praesent vitae vestibulum ligula, et consequat enim. Duis maximus nulla sapien, imperdiet efficitur metus dapibus vel. Donec augue ante, viverra porta sapien at, maximus malesuada lorem. Integer maximus, nisi non vulputate euismod, felis massa dapibus velit, ac laoreet justo eros id ex. Phasellus sapien augue, fermentum vel sem sit amet, porta efficitur sapien. Aenean at lacus nec quam pretium pharetra. Pellentesque eleifend quam ut ante sagittis tincidunt. Nam in metus in eros faucibus rhoncus id pretium felis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam feugiat arcu et ornare viverra. Morbi fermentum dui ipsum, vel blandit mauris convallis et. Maecenas ut orci sem. Vivamus dolor neque, fermentum porta nulla luctus, dapibus placerat eros. Sed a quam sed justo semper aliquet non sit amet magna. In at tempus ex.', # noqa
                enable_email_notification=True,
                allow_user_to_choose_predictor=False,
                allow_user_to_choose_number_of_tweets=True,
                default_predictor=predictor
            )
            self.stdout.write(self.style.SUCCESS('App table seeded!'))

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        self.seed_user()
        self.seed_predictor()
        self.seed_app()
        self.stdout.write('Database seeded!')
