from django.contrib import admin

from .models import User, Category, Transaction

admin.site.register([User, Category, Transaction])
