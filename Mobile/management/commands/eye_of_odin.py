from django.core.management.base import BaseCommand, CommandError

from Scraper.models import OdinList, EmailModel
from Scraper.page_links import get_emails_from_page

class Command(BaseCommand):
    help = 'Check the domain to scrape'

    def handle(self, *args, **options):
        try:
            # Get all urls to scrape
            urls = OdinList.objects.all()

            for url in urls:
                # if url.need_scrape():
                emails = get_emails_from_page(url.domain)
                for i in emails:
                    sp = i.split('@')
                    name = sp[0]
                    domain = sp[-1]

                    # Adding to database
                    obj = EmailModel.objects.create(email=i, name=name, domain=domain)
                    obj.validate()
        except:
            raise CommandError('Something went wrong here.')