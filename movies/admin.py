from django.contrib import admin
from movies.models import *

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(User)