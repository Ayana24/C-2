# models.py

from django.db import models

# Пользователь
class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email

# Координаты
class Coord(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

# Перевал
class PerevalAdded(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('pending', 'В работе'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perevals')
    coords = models.OneToOneField(Coord, on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)

    level_winter = models.CharField(max_length=10, blank=True)
    level_summer = models.CharField(max_length=10, blank=True)
    level_autumn = models.CharField(max_length=10, blank=True)
    level_spring = models.CharField(max_length=10, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

# Изображения
class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=255, blank=True)
    data = models.ImageField(upload_to='images/')

