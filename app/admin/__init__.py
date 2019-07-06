from django.contrib import admin
from .. import models

# Import your custom admin classes here.
admin.site.register(models.User)
