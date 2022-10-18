from django.contrib import admin
from django.contrib.admin.options import ModelAdmin


# Register your models here.
from .models import cart
from .models import customer
from .models import product
from .models import orderplaced

class customerAdmin(admin.ModelAdmin):
         list_display=('id','user','name','locality','city','zipcode','state')
admin.site.register(customer,customerAdmin)

class cartAdmin(admin.ModelAdmin):
         list_display=('id','user','product','quantity')
admin.site.register(cart,cartAdmin)

class productAdmin(admin.ModelAdmin):
         list_display=('id','title','selling_price','discount_price','description','brand','category','product_image')
admin.site.register(product,productAdmin)

class orderplacedAdmin(admin.ModelAdmin):
         list_display=('id','user','customer','product','quantity','ordered_date','status')
admin.site.register(orderplaced,orderplacedAdmin)