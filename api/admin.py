from django.contrib import admin
from .models import User, Coord, PerevalAdded, PerevalImage

admin.site.register(User)
admin.site.register(Coord)
admin.site.register(PerevalAdded)
admin.site.register(PerevalImage)