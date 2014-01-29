from django.core.management.base import BaseCommand
from juck.accounts.models import Manager


class Command(BaseCommand):
    def handle(*args, **options):
        manager = Manager.objects.create(email='mo@dir.com')
        manager.set_password('1234')
        manager.save()