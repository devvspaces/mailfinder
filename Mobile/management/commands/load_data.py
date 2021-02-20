from django.core.management.base import BaseCommand, CommandError

from Scraper.models import EmailModel

class Command(BaseCommand):
    help = 'Loading current email set to database'

    def handle(self, *args, **options):
        try:
            # Get all data first
            with open('email.csv','r') as f:
                data = list(set([i.replace('\n','') for i in f.readlines()]))
            
            for b,i in enumerate(data,1):
                try:
                    sp = i.split('@')
                    name = sp[0]
                    domain = sp[-1]
                    obj = EmailModel.objects.create(email=i,name=name,domain=domain)
                except:
                    pass
                print(b)
            
            print('Data completely loaded')
        except:
            raise CommandError('Something went wrong here.')