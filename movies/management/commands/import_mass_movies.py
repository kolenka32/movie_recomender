from django.core.management.base import BaseCommand
from movies.services.bulk_import_service import import_mass_movies


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        import_mass_movies()