from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize the database.'

    @staticmethod
    def handle(*args, **options):
        from base.utilities import initialize_database
        initialize_database()
        # Optionally, you can add print statements or log messages here to indicate that the command was executed successfully.
        print("Database initialized successfully.")
