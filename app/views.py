# from django.conf import settings
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse 
from .models import*
from django.core.mail import send_mail
import random
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.paginator import Paginator
import razorpay

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import check_password

# Create your views here.
@never_cache
def index(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        
        count=addcart.objects.filter(user=uid).count()
        pp=product.objects.all().order_by("-id")
        con={"pp":pp,"count":count,"w_count":w_count}
        return render(request,"index.html",con)
    
    else:
        return render(request,"login.html")


def cart(request):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        count = addcart.objects.filter(user=uid).count()
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        
        mid = main_category.objects.all()
        ct = addcart.objects.filter(user=uid)

        print(ct)

        sub_total = 0
        charge = 50
        l1 = []
        t_price = 0  

        for i in ct:
            a = i.t_price
            l1.append(a)
            sub_total = sum(l1)
            t_price = sub_total + charge

        contaxt = {'mid': mid,
                'ct': ct,
                'sub_total': sub_total,
                'charge': charge,
                't_price': t_price,
                'count': count,
                "w_count":w_count}

        return render(request, "cart.html", contaxt)
    else:
        return render(request,"login.html")




def add_to_cart(request, id):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        pid = product.objects.get(id=id)
        aid = addcart.objects.filter(products=pid, user=uid).exists()

        if aid:
            messages.info(request, "Product Is Already Exists")
        else:
            addcart.objects.create(
                user=uid,
                products=pid,
                price=pid.price,
                name=pid.name,
                quantity=1,
                img=pid.img,
                t_price=pid.price
            )
            messages.success(request, "Product added to cart successfully.")

        # ✅ Redirect to the page where the user came from
        next_url = request.GET.get('next', 'cart')
        return redirect(next_url)
    else:
        return render(request,"login.html")        




def shop_add_to_card(request,id):

    pp=addcart.objects.get(id=id)
    
    contaxt={
        'pp':pp,
      
    }
    return render(request,"detail.html",contaxt)


def cart_plus(request,id):
    cart=addcart.objects.get(id=id)
    if cart:
        cart.quantity +=1
        cart.t_price=cart.quantity*cart.price
        cart.save()
        return redirect("cart")
    else:
        return redirect("cart")

def cart_mines(request,id):
    cart=addcart.objects.get(id=id)
    if cart:
        if(cart.quantity==1):
            addcart.objects.get(id=id).delete()
        else:
            cart.quantity-=1
            cart.t_price=cart.quantity*cart.price
            cart.save()
        return redirect("cart")
    else:
         
        return redirect("cart")







def delete1(request,id):
    dell=addcart.objects.filter(id=id)
    dell.delete()
    return redirect("cart")

def order_delete(request,id):
    dell=Order.objects.filter(id=id)
    dell.delete()
    return redirect("order1")




import razorpay
def checkout(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        aid=addcart.objects.filter(user=uid)
        count=addcart.objects.filter(user=uid).count()
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        
        l1=[]
        sub_total=0
        charge=50
        dis=0
        t_price = 0
        for i in aid:
            l1.append(i.t_price)
            sub_total=sum(l1)
            print(sub_total)
            discount=0
            dis=None
            t_price=sub_total+charge
            
            if sub_total==0:
                charge=0
                t_price=0
            else:
                charge=50
            if "discount" in request.session:
                dis=request.session.get('discount')
                t_price=sub_total+charge-dis
                print(dis)
            else:
                dis=0
                t_price=sub_total+charge
            if t_price==0:
                con={"aid":aid,
                    "sub_total":sub_total,
                    "charge":charge,
                    "t_price":t_price,
                    "uid":uid,
                    "discount":dis,
                    'count':count,
                    "w_count":w_count}
                return render(request,"checkout.html",con)
        else:
            amount = max(t_price, 1) * 100
            client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE','77yKq3N9Wul97JVQcjtIVB5z'))
            response = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})
                
            print(response,"**************")
            contaxt={
                "aid":aid,
                "sub_total":sub_total,
                "charge":charge,
                "t_price":t_price,
                "uid":uid,
                "response":response,
                "discount":dis,
                'count':count,
            }
            return render(request,"checkout.html",contaxt)
    else:
        return render(request,"login.html")        





def billing_view(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        aid=addcart.objects.filter(user=uid)
        a_count=addcart.objects.filter(user=uid).count()
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
                
        count=addcart.objects.filter(user=uid).count()
        if 'discount' in request.session:
            del request.session['discount']
        
        for i in aid:
            Order.objects.create(user=uid,
                                
                                product_name=i.name,
                                img=i.img,
                                price=i.price,
                                qtn=i.quantity,
                                t_price=i.t_price)
            i.delete()
        if request.POST:
            f_name=request.POST['f_name']
            l_name=request.POST['l_name']
            company_name=request.POST['company_name']
            
            country=request.POST['country']
            address=request.POST['address']
            city=request.POST['city']

            zip_code=request.POST['zip_code']
            mobile=request.POST['mobile']
        
            
            billing_address.objects.create(user=uid,f_name=f_name,l_name=l_name,company_name=company_name,country=country,address=address,city=city,zip_code=zip_code,mobile=mobile,email=uid.email)
            con={'count':count,"w_count":w_count}
            return render(request,"checkout.html",con)
        else:
            con={'count':count}
            return render(request,"checkout.html",con)
    else:
        return render(request,"login.html")        


def show_orders(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        ord1=Order.objects.filter(user_id=uid)
        con={"ord1":ord1}
        return render(request,"order.html",con)
    else:
        return render(request,"login.html")        



def apply_coupon(request):
    uid=User.objects.get(email=request.session['email'])
    aid=addcart.objects.filter(user=uid)
    a_count=addcart.objects.filter(user=uid).count()        
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    l1=[]
    sub_total=0
    charge=50
    for i in aid:
        l1.append(i.t_price)
    print(l1)
    sub_total=sum(l1)
    print(sub_total)
    t_price=sub_total+charge
    discount=0
    if request.POST:
        coupon=request.POST['code']
        print(coupon)
        caid=coupon_code.objects.filter(code=coupon).exists()
        print(caid)
        if caid:
            cid=coupon_code.objects.get(code=coupon)
            t_price-=cid.discount
            discount=cid.discount
            request.session['discount']=discount
            contaxt={
            "uid":uid,
            "aid":aid,
            "a_count":a_count,
            "sub_total":sub_total,
            "t_price":t_price,
            "charge":charge,
            "discount":discount,
            "w_count":w_count}
            
            messages.info(request,"Coupon Code Apply Successfully")
            return render(request,"cart.html",contaxt)

        else:
            contaxt={
            "uid":uid,
            "aid":aid,
            "a_count":a_count,
            "sub_total":sub_total,
            "t_price":t_price,
            "charge":charge,
            "discount":0,
            }
            messages.info(request,"No Coupons")
            return render(request,"cart.html",contaxt)
            
    else:   
        
        return render(request,"cart.html")



def error404(request):
    return render(request,"error404.html")


def shop_detail(request):
    uid=User.objects.get(email=request.session['email'])
    count=category.objects.filter(name1=uid).count()
    count=addcart.objects.filter(user=uid).count()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()
    
    con={'count':count,
         'count':count,
         "w_count":w_count}
    return render(request,"shop_detail.html",con)

def shop_detail1(request,id):
    uid=User.objects.get(email=request.session['email'])
    count=category.objects.filter(name1=uid).count()
    count=addcart.objects.filter(user=uid).count()
    cat=category.objects.all()
    cat2=request.GET.get("cat2") 
    pp=product.objects.get(id=id)
    mid=main_category.objects.all()
    w_count=Add_Whishlist.objects.filter(user_id=uid).count()

    
    
    contaxt={'pp':pp,
            'mid':mid,
            'cat':cat,
            'cat2':cat2,
            'count':count,
            'count':count,"w_count":w_count}
    return render(request,"shop_detail.html",contaxt)

def shop(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        count=category.objects.filter(name1=uid).count()
        count=addcart.objects.filter(user=uid).count()
        pp=product.objects.all().order_by("-id")
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        whishlist_product=Add_Whishlist.objects.filter(user_id=uid)
        l1=[]
        for i in whishlist_product:
            l1.append(i.product_id.id)
        
        mid=main_category.objects.all()
        cid=request.GET.get("cid")
        
        piz=price.objects.all()
        piz2=request.GET.get("piz2")

        cat=category.objects.all()
        cat2=request.GET.get("cat2") 
        
        S=request.GET.get("sort")
        
        if cid:
            pp=product.objects.filter(sub_category=cid)
        elif piz2:
            pp=product.objects.filter(price1=piz2)
        elif cat2:
            pp=product.objects.filter(name1=cat2)
        elif S=="lth":
            pp=product.objects.all().order_by("price") 
        elif S=="htl":
            pp=product.objects.all().order_by("-price")  
        elif S=="atz":
            pp=product.objects.all().order_by("name")
        elif S=="zta":
            pp=product.objects.all().order_by("-name")
        else:
            pp=product.objects.all().order_by("-id")
        
        paginator=Paginator(pp,3)  
        page_number=request.GET.get("page",1)  
        pp=paginator.get_page(page_number)
        show_page=paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)
        con={'pp':pp,
            'mid':mid,
            'cat':cat,
            'piz':piz,
            "min1":0,
            'count':count,
            'count':count,
            "w_count":w_count,
            "whishlist_product":whishlist_product,"l1":l1,"show_page":show_page}
        return render(request,"shop.html",con)
    else:
        return render(request,"login.html")



def filter_price(request):
    if request.POST:
        max1=request.POST['max1']
        print(max1)
        pp=product.objects.filter(price__lte=max1) 
        print(pp)
        contaxt={                         
            "pp":pp,
            "max1":max1,
        
                
        }
        return render(request,"shop.html",contaxt)
    else:
        contaxt={
        
            "min1":None
            
        }
        return render(request,"shop.html",contaxt)



def price1(request):
    price=request.GET.get("price")
    print(price)
    pid=product.objects.filter(price__lte=price)
    print(pid)
    contaxt={
        "pid":pid
    }
    return render(request,"shop.html",contaxt)
    
def search(request):
    srh=request.GET.get("srh")
    print(srh)
    if srh:
        pid=product.objects.filter(name__icontains=srh)
        print(pid)
    con={"pid":pid,"srh":srh}
    return render(request,"shop.html",con)

def testimonial(request):
    return render(request,"testimonial.html")


def logout(request):
     
        del request.session['email']
        return redirect("login")






def login(request):
    if 'email' in request.session:
        return redirect("index")  # already logged in

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):  # ✅ check hashed password
                request.session['email'] = user.email
                return redirect("index")
            else:
                return render(request, "login.html", {"e_msg": "Invalid password."})
        except User.DoesNotExist:
            return render(request, "login.html", {"e_msg": "Invalid email."})
    
    return render(request, "login.html")

 
def confirm_password(request):
    if request.POST:
        email=request.POST.get('email')
        otp=request.POST.get('otp')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        
        print(email,otp)
        try:
            uid=User.objects.get(email=email)
            if str(uid.otp)==otp:
                print(otp)
                if new_password==confirm_password:
                   uid.password=new_password
                   uid.save()
                   con={'email':email,'uid':uid,'emsg':'password change successfully'}
                   return render(request,"login.html",con)
                else:
                    con={'email':email,
                         'emsg':'password do not match'}
                    return render(request,"confirm_password.html",con)
            else:
                con={'email':email,
                     'emsg':'Invalid OTP'}
                return render(request,"confirm_password.html",con)
        except:
            con={'email':email,
             'emsg':'user not found'}
            return render(request,"confirm_password.html",con)
              
    return render(request,"confirm_password.html")     

#===============================================================    


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
import random
from django.contrib.auth.models import User


# For demo only. In production, use a persistent store like DB or Redis
otp_storage = {}

def forget(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Step 1: User enters email ➝ send OTP
        if email and not otp:
            try:
                user = User.objects.get(email=email)
                generated_otp = str(random.randint(100000, 999999))
                otp_storage[email] = generated_otp

                send_mail(
                    'Your OTP for password reset',
                    f'Your OTP is: {generated_otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                return render(request, "forget.html", {
                    "msg": "OTP sent to your email.",
                    "email_entered": True,
                    "email": email
                })

            except User.DoesNotExist:
                return render(request, "forget.html", {
                    "msg": "Email not registered."
                })

        # Step 2: OTP + Password reset
        elif email and otp and new_password and confirm_password:
            stored_otp = otp_storage.get(email)

            if stored_otp and otp == stored_otp:
                if new_password == confirm_password:
                    try:
                        user = User.objects.get(email=email)
                        user.set_password(new_password)  # Securely set password
                        user.save()
                        otp_storage.pop(email, None)  # Clean up OTP
                        return redirect("login")  # Replace with your login URL name
                    except User.DoesNotExist:
                        return render(request, "forget.html", {
                            "msg": "User not found."
                        })
                else:
                    return render(request, "forget.html", {
                        "msg": "Passwords do not match.",
                        "email_entered": True,
                        "email": email
                    })
            else:
                return render(request, "forget.html", {
                    "msg": "Invalid OTP.",
                    "email_entered": True,
                    "email": email
                })

    return render(request, "forget.html")

        
#===============================================================


from django.shortcuts import render, redirect
from .models import User
import requests
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"e_msg": "Email already exists."})

        if password != c_password:
            return render(request, "register.html", {"e_msg": "Passwords do not match."})
        
        else:
            User.objects.create(name=name, email=email, password=make_password(password))
            return redirect("login")

        # if User.objects.filter(email=email).exists():
        #     return render(request, "register.html", {"e_msg": "Email already exists."})

        # if password != c_password:
        #     return render(request, "register.html", {"e_msg": "Passwords do not match."})
        

        # try:
        #     res = requests.get(
        #         "https://emailvalidation.abstractapi.com/v1/",
        #         params={"api_key": "6089bc4afeb248cfbae263ac6dd99ef8", "email": email}
        #     )
        #     print(res)
        #     if res.status_code == 200:
        #         User.objects.create(name=name, email=email, password=make_password(password))
        #         return redirect("login")
        # except:
        #     pass

        # return render(request, "register.html", {"e_msg": "Invalid or undeliverable email."})

    return render(request, "register.html")



   

def contact(request):
    if 'email' in request.session:
        uid = User.objects.get(email=request.session['email'])
        count=addcart.objects.filter(user=uid).count()
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        
        if request.POST:
            name=request.POST['name']
                    
            email=request.POST['email']  
                
            message=request.POST['message']  
            
            Contact.objects.create(name=name,email=email,message=message) 
        con={"count":count,
            "uid":uid,"w_count":w_count}
        return render(request,"contact.html",con)        
    else:
        return render(request,"login.html")        

                    

def Whishlist(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        w_count=Add_Whishlist.objects.filter(user_id=uid).count()
        count = addcart.objects.filter(user=uid).count()
        
        whish=Add_Whishlist.objects.filter(user_id=uid)
        con={"uid":uid,"whish":whish,"w_count":w_count,"count":count}
        return render(request,"whishlist.html",con)
    else:
        return render(request,"login.html")        




def add_whishlist(request, id):
    uid = User.objects.get(email=request.session['email'])
    pp = product.objects.get(id=id)
    w_id = Add_Whishlist.objects.filter(product_id=pp, user_id=uid).first()
    
    if w_id:
        w_id.delete()
        messages.info(request, "Item Removed From Your Wishlist")
    else:
        Add_Whishlist.objects.create(
            user_id=uid,
            product_id=pp,
            price=pp.price,
            name=pp.name,
            image=pp.img)
        messages.info(request, "Item Saved In Your Wishlist")
        
    return redirect("shop")

    

def remove_whishlist(request, id):
    
    
    c=Add_Whishlist.objects.get(id=id)
    c.delete()
    return redirect('Whishlist')




