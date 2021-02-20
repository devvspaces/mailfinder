import json
from django.core.management.base import BaseCommand, CommandError

from Scraper.models import EmailModel

class Command(BaseCommand):
    help = 'Loading current email set to database'

    def handle(self, *args, **options):
        try:
            # Get all data first
            with open('dataset.json','r') as f:
                data = list(set([i.replace('\n','') for i in f.readlines()]))
            
            for b,i in enumerate(data,1):
                try:
                    line = json.loads(i)
                    email = line['email']
                    username = line['username']
                    country = line['country']
                    domain = email.split('@')[-1]
                    obj = EmailModel.objects.create(email=email,name=username,domain=domain,country=country)
                except:
                    pass
                
                line = ''
                
                if str(b).endswith('00'):
                    print(b)
            
            print('Data completely loaded')
        except:
            raise CommandError('Something went wrong here.')