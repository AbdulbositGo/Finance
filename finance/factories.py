import factory
import random
from django.utils import timezone
from datetime import datetime
from .models import User, Category, Transaction


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'finance.User'
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    user_name = factory.Sequence(lambda n: f"user{n}")

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Iterator(
        [
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
    )

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = factory.LazyFunction(lambda: random.uniform(1, 2500))
    date_time = timezone.make_aware(
        factory.Faker(
            'date_time_between',
            start_date=datetime(year=2024, month=1, day=1, hour=1),
            end_date=datetime.now(),
        )
    )
    type = factory.Faker(
        'random_element',
        elements = [
            x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES
        ]
    )


