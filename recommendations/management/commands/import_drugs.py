from django.core.management.base import BaseCommand
import pandas as pd
from recommendations.models import Drug


class Command(BaseCommand):
    help = 'Import drugs from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'recommendations/management/commands/output_dataset.csv'
        data = pd.read_csv(file_path)

        # 遍历数据集并插入到数据库
        for _, row in data.iterrows():
            Drug.objects.create(
                name=row['name'],
                description=row.get('description'),
                reason=row.get('reason'),
                company=row.get('company'),
                rating=row.get('rating')
            )

        self.stdout.write(self.style.SUCCESS('数据已成功导入数据库！'))
