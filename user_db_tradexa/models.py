from django.db import models

class User(models.Model):
    name = models.CharField(max_length=15)
    email = models.TextField()

    class Meta:
        app_label = 'user_db_tradexa'

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    class Meta:
        app_label = 'user_db_tradexa'

class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()


    class Meta:
        app_label = 'user_db_tradexa'

