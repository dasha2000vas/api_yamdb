import csv
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help_cmd = 'Импорт данных из файлов CSV в БД'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='путь к файлу CSV')
        parser.add_argument('model', type=str, help='имя модели')

    def handle(self, *args, **options):
        file_path = options['path']
        model_name = options['model']
        model = apps.get_model(model_name)

        def process_csv_row(row, header):
            return {key: value for key, value in zip(header, row)}

        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            header = next(reader)
            for row in reader:
                data = process_csv_row(row, header)
                try:
                    model.objects.create(**data)
                except IntegrityError as err:
                    line = ', '.join(row)
                    self.stdout.write(f'Error! {err}, "{line}"')
