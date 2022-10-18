from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
STATE_CHOICES =(
       ('andman &nicobar islands','andman &nicobar islands'),
       ('bihar','bihar'),
       ('andhra pradesh','andhra pradesh'),
       ('assam','assam'),
       ('chandighar','chandighar'),
       ('delhi','delhi'),
       ('dadra ','dadra'),
 )
class customer(models.Model):
      #  amount=models.IntegerField(default=0)
       user  =models.ForeignKey(User, on_delete=models.CASCADE)
       name =models.CharField(max_length=100)
       locality = models.CharField(max_length=100)
       city = models.CharField(max_length=30)
       zipcode =models.IntegerField()
       state =models.CharField(choices=STATE_CHOICES,max_length=50)

def __str__(self): 
      return  str(self.id)

CATEGORY_CHOICES =(
      ('M','mobile'),

      ('L','laptop'),
      ('TW','top wear'),

      ('BW','bottom wear')
)

class product(models.Model):
      title=models.CharField(max_length=100)
      selling_price=models.FloatField()
      discount_price=models.FloatField()
      description=models.TextField()
      brand=models.CharField(max_length=100)
      category=models.CharField( choices=CATEGORY_CHOICES ,max_length=2)
      product_image=models.ImageField(upload_to='productimg')

def __str__(self):
      return str(self.id)

class cart(models.Model):
         user=models.ForeignKey(User,on_delete=models.CASCADE)
         product=models.ForeignKey(product ,on_delete=models.CASCADE)  
         quantity=models.PositiveIntegerField(default=1) 

def __str__(self):
      return   str(self.id)

      @property
      def total_cost(self):
       return self.quantity*self.product.discount_price

STATUS_CHOICES     = (
('accepted','accepted'),
('packed','packed'),
('on  the way','on the way'),
('delivered','delivered'),
('cancel','cancel')
) 

class orderplaced(models.Model):
      user =models.ForeignKey(User, on_delete=models.CASCADE)
      customer=models.ForeignKey(customer, on_delete=models.CASCADE)
      product=models.ForeignKey(product, on_delete=models.CASCADE)
      quantity= models.PositiveIntegerField(default=1)
      ordered_date=models.DateTimeField(auto_now_add=True)
      status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')


      @property
      def total_cost(self):
       return self.quantity*self.product.discount_price

