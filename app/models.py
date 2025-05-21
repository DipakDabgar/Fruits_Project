from django.db import models
from django.forms import BaseModelForm
from django.contrib.auth.models import User



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Now you can use this!
        user.save()
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=30)
    name = models.CharField(max_length=255)
    otp = models.IntegerField(default=123)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


   
        
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=30)
    message=models.TextField()
    
    def __str__(self):
        return self.name
    
class price(models.Model):
    price1 = models.CharField(max_length=50)   
    
    def __str__(self) -> str:
        return self.price1
    
    
class main_category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class sub_category(models.Model):
       main_category=models.ForeignKey(main_category,on_delete=models.CASCADE) 
       name=models.CharField(max_length=50)

       def __str__(self) -> str:
           return self.name

class category(models.Model):
    name1=models.CharField(max_length=30)
      
    def __str__(self):
          return self.name1

class product(models.Model):
    main_category=models.ForeignKey(main_category,on_delete=models.CASCADE,blank=True,null=True)
    sub_category=models.ForeignKey(sub_category,on_delete=models.CASCADE,blank=True,null=True)
    price1=models.ForeignKey(price,on_delete=models.CASCADE,blank=True,null=True)
    name1=models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    img=models.ImageField(upload_to='media')
    star=models.IntegerField(default=0)
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    des=models.TextField(blank=True,null=True)
    
    
    def __str__(self):
        return self.name    


    
class addcart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(product, on_delete=models.CASCADE)
 
    img=models.ImageField(upload_to='media',blank=True,null=True)
    price=models.IntegerField()
    t_price=models.IntegerField()
    name=models.CharField(max_length=30)
    quantity=models.IntegerField()
    datetime=models.DateTimeField(auto_now=True,blank=True,null=True)
     
    
    def __str__(self) -> str:
        return self.name
     
     
    
class billing_address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    f_name=models.CharField(max_length=50)
    l_name=models.CharField(max_length=50)
    company_name=models.CharField(max_length=50)
    address=models.TextField()
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    zip_code=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    
    
    
    def __str__(self):
        return self.f_name
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    order_id=models.CharField(max_length=40,blank=True,null=True)
    img=models.ImageField()
    product_name=models.CharField(max_length=40)
    price=models.IntegerField()
    qtn=models.IntegerField()
    t_price=models.IntegerField()
    datetime=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    
    def __str__(self):
        return self.product_name

    
# class coupon(models.Model):
#     code=models.CharField(unique=True,max_length=10)
#     discount_amount=models.IntegerField()
#     min_order_amount=models.IntegerField()
#     max_order_amount=models.IntegerField()
#     expiry_date=models.DateTimeField()

#     def __str__(self):
#         return self.code       


class coupon_code(models.Model):
    code=models.CharField(max_length=10)
    discount=models.IntegerField()

    def __str__(self):
        return self.code
        

class Rating(models.Model):
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])    

    def __int__(self) -> str:
        return self.rating
    
         
    
class Add_Whishlist(models.Model):
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,blank=True,null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(upload_to="media",null=True,blank=True)
 
    name=models.CharField(max_length=60,null=True,blank=True)
    price=models.IntegerField()
    
     
    def __str__(self):
        return self.name
    
    
    

