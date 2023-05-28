from django.contrib.auth.models import Group, User #importa los modelos Group y user
from django.db import models #importa los metodos necesarios para trabajar con modellos


def custom_upload_to(instance, filename):
     return 'product/' + filename
       



