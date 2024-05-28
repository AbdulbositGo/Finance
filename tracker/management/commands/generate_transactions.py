import random 
from faker import Faker
from datetime import datetime
from django.core.management.base import BaseCommand

from tracker.models import Category, Transaction, User


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        categories = [
            'Bills',
            'Food',
            'Clothes',
            'Medical',
            'Hausing',
            'Salary',
            'Social',
            'Transport',
            'Vacation',
            'Internet',
            'Books',
            'Phone',
            'Grocery',
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)
        
        user = User.objects.filter(username="admin").first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='1')

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for i in range(50):
            Transaction.objects.create(
                category=random.choice(categories),
                user=user,
                amount=random.uniform(1, 2500),
                time=fake.date_time_between(start_date="-1y", end_date="now"),
                type=random.choice(types)
            )
