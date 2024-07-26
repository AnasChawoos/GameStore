from django.shortcuts import render,HttpResponse,redirect
from GamestoreApp.models import Product,Cart,Orders,Reviews
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import get_connection, EmailMessage
import random
# Create your views here.

def Anas(request):
    
    return render(request, "A.html")

def B(request):
    
    if request.method=="GET":
        
        return render(request, "AddGame.html")
    
    
    else:
        
        name=request.POST['name']
        description=request.POST['description']
        manufacturer=request.POST['manufacturer']
        category=request.POST['category']
        price=request.POST['price']
        image=request.FILES['image']
        
        
        p=Product.objects.create(name=name, description=description, manufacturer=manufacturer, category=category, price=price, image=image)
        p.save()
        
        return redirect('/H')
    
    
    
def S(request):
    
    if request.method=="GET":
        
        
    
        p=Product.objects.all()
        
        context={'data': p} 
        
        return render(request, "Read.html" , context) 
    
    else:
        
        name=request.POST['search']
        
        p=Product.objects.get(name=name)
        
        return redirect(f"RPD/{p.id}")
     


def Update(request, rid):
    if request.method =="GET":
    
        p=Product.objects.filter(id=rid)
        
        context={'data': p} 
        
        return render(request, "Updated.html" , context) 
    
    else:
        name=request.POST['uname']
        description=request.POST['udescription']
        manufacturer=request.POST['umanufacturer']
        category=request.POST['ucategory']
        price=request.POST['uprice']
        image=request.FILES['uimage']
        
        p=Product.objects.filter(id=rid)
        p.update(name=name, description=description, manufacturer=manufacturer, category=category, price=price, image=image)
       
        
        return redirect('/H')
    
def Delete(request ,rid):
    
    p=Product.objects.filter(id=rid)
    p.delete()   
    
    return redirect("/H") 


def R(request):
    
    if request.method=="GET":
        
        
        
        return render(request, "Register.html")
    
    else:
        
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        
        if password==confirm_password:
            u=User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            u.set_password(password)
            u.save()
            
            return redirect('/')
        
        else:
            
            context={}
            context['error']="Password and Confirm Password doesn't match"
            
            return render(request, "Register.html", context)
        
        
        
def User_Login(request):
    
    if request.method=="GET":
        
        return render(request, "Login.html")
    
    else:
        
        username=request.POST['username']
        password=request.POST['password']
        
        a=authenticate(username=username, password=password)
        if a is  not None:
            login(request, a)
            return redirect("/")
            
        else:
            
            context={"error":"USername and Password Incorrect"}
            return render(request, "Login.html", context) 
        
        
def Logout(request):
    
    logout(request)
    
    return redirect('/')  

@login_required(login_url='/L')
def Carty(request, rid):
    
    p=Product.objects.get(id=rid)
    cart_pro=Cart.objects.filter(product=p, user=request.user ).exists()
    if cart_pro:
        return redirect('/P')
    else:
        
        u=User.objects.get(username=request.user) 
        total_price=p.price
        
        c=Cart.objects.create(product=p, user=u, quantity=1, total_price=total_price)
        c.save()
        
        return redirect('/P')
    
@login_required(login_url='/L')   
def RC(request):
    
    c=Cart.objects.filter(user=request.user)
    context={'data':c} 
    
    total_quantity=0
    total_price=0
    
    for x in c:
        total_quantity+= x.quantity
        total_price+= x.total_price
    context['total_quantity']=total_quantity
    context['total_price']=total_price
        
    
    return render(request, "read_cart.html", context)  


def T(request, rid):
    
    c=Cart.objects.filter(id=rid)
    c.delete()
    
    return redirect('/H') 


def Update_cart(request, rid, q):
    
    cart=Cart.objects.filter(id=rid)
    c=Cart.objects.get(id=rid)
    quantity=int(q)
    price=int(c.product.price)*quantity
    cart.update(quantity=q, total_price=price)
    
    
    return redirect('/P')


def CO(request, rid):
    
    cart=Cart.objects.get(id=rid)
    orders=Orders.objects.create(product=cart.product, user=cart.user, quantity=cart.quantity, total_price=cart.total_price)
    orders.save()
    cart.delete()
    
    return redirect('/P')

@login_required(login_url='/L')
def Read_O(request):
    
    o=Orders.objects.filter(user=request.user)
    
    context={"data":o}
    
    return render(request, "Read_Orders.html", context)



def RRO2(request, rid):
    prod=Product.objects.get(id=rid)
    
    rev=Reviews.objects.filter(user=request.user, product=prod).exists()
    if rev:
        return HttpResponse("Already Review Added")
    
    else:
    
      if request.method=="GET":
    
       return render(request, "Review.html")
   
   
      else:
        
        title=request.POST['title']
        content=request.POST['content']
        rating=request.POST['rate']
        image=request.FILES['image']
        
        
        prod=Product.objects.get(id=rid)
        
        review=Reviews.objects.create(product=prod ,user=request.user, title=title, content=content, rating=rating, image=image)
        review.save()
        
        return HttpResponse("Review added")
    
    
def ReadPD1(request, rid):
    
    prod=Product.objects.filter(id=rid)
    
    p=Product.objects.get(id=rid)
    n=Reviews.objects.filter(product=p).count()
    rev=Reviews.objects.filter(product=p)
    
    sum=0
    for x in rev:
        
        sum+=x.rating
        
    try:
            
        
          avg_r=sum/n
        
          avg=int(sum/n)
    except:
        print("No Review")    
        
    context={}  
    context['data']=prod 
    if n==0:
        context['avg']="No Review" 
    else:    
        context['avg_rating']=avg 
        context['avg']=avg_r
    
    return render(request, "ReadPD.html", context) 


def FP1(request):
    
    if request.method=="GET":
        
        
    
       return render(request, "FOP.html")  
   
    else:
        
        email=request.POST['email']
        
        request.session['email']=email
        
        user=User.objects.filter(email=email).exists()
        
        if user:
        
            otp= random.randint(1000,9999)
            
            request.session['otp']=otp
            
            with get_connection(
                host=  settings.EMAIL_HOST,
                port= settings.EMAIL_PORT,
                username= settings.EMAIL_HOST_USER,
                password=   settings.EMAIL_HOST_PASSWORD,
                use_tls= settings.EMAIL_USE_TLS
            )as connection :
                
                subject= "OTP Verification"
                email_from= settings.EMAIL_HOST_USER
                receiption_list= [email]
                message= f"OTP is {otp}"
                
                EmailMessage(subject, message, email_from, receiption_list, connection=connection).send()
            
            
                return redirect("/Verification_OTP")
            
        else:
            context={}
            
            context['error']= 'User does not exists'
            
            return render(request, "FOP.html", context)    
        
        
def OTP(request):
    
    if request.method=='GET':
        
        return render(request, "OTp.html")
    
    else:
        
        otp=int(request.POST['otp'])
        email_otp=int(request.session['otp'])
        
        if otp == email_otp:
            return redirect('/NP')
        else:
            return HttpResponse("Not Ok")
        
        
def New_Password(request):
    
    if request.method=="GET":
        
        return render(request, "New_password.html")
    
    else:
        email=request.session['email']
        
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
       
        user=User.objects.get(email=email)
        
        if new_password==confirm_password:
            
            user.set_password(new_password)
            user.save()
            
            return redirect('/L')
        
        else:
            
          context={"error":"Password and Confirm Password Does Not match"}
          
          return render(request, "New_password.html", context)
            
        
        
        
                   
                    
            
            
            
            
        
         
        
     
        
