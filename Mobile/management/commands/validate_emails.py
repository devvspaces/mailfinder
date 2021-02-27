from django.core.management.base import BaseCommand, CommandError

from Scraper.models import EmailModel

class Command(BaseCommand):
    help = 'We will validate emails that have passed their time validation'

    def handle(self, *args, **options):
        try:
            # Get all data first
            objs = EmailModel.objects.all()
            for i in objs:
                i.validate()
        except:
            raise CommandError('Something went wrong here.')