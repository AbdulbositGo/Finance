import random
from faker import Faker
from django.core.management.base import BaseCommand
from finance.models import User, Transaction, Category
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generates transaction for testing'

    def handle(self, *args, **options):
        fake = Faker()

        categories = [
            'Bills',
            'Food',
            'Clothes',
            'Medical',
            'Housing',
            'Salary',
            'Social',
            'Transport',
            'Vacation',
        ]
        for category in categories:
            Category.objects.get_or_create(name=category)

        # get the user
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='1')
        
        categories = Category.objects.all()
        transactions = []
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for _ in range(5):
            transactions.append(
                Transaction(
                    category=random.choice(categories),
                    user=user,
                    amount=random.uniform(1, 2500),
                    date_time=timezone.make_aware(fake.date_time_between(start_date="-1y", end_date='now')),
                    type=random.choice(types)
                )
            )
        Transaction.objects.bulk_create(transactions)
        print('Done ✅')