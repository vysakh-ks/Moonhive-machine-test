from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def index(request):
    if request.method == 'POST':
       
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('core:home') 
        else:
            messages.error(request, 'Invalid email or password.')
        return redirect('core:index')
    else:
        return render(request, 'index.html')
    
@login_required(login_url='core:index')
def home(request):
    if request.method == 'POST':
        key = request.POST['key']
        print(key)

        try:
            property = Property.objects.filter(Q(features__icontains=key) | Q(name__icontains=key))
        except:
            property=""
    else:
        property = Property.objects.all()
   
    
    context = {'property':property}

    return render(request,'home.html',context)

@login_required(login_url='core:index')
def view_prop(request,prop):
    property = Property.objects.filter(id=prop).first()

    try:
        unit = Unit.objects.filter(property=property)
    except:
        messages.info(request,'No units vailable in this property')
    tenant_det = []
    for un in unit:
        try:
            tenant = Tenant.objects.filter(unit = un) #[tenant1]
            new_unit={"unit":un,"tenant":tenant.first()}
            tenant_det.append(new_unit)
        except:
            pass

    context = {'tenant_det':tenant_det,'property':property}
    return render(request,'viewproperty.html',context)

@login_required(login_url='core:index')
def tenant_view(request):
    tenant = Tenant.objects.all()
    context = {'tenant':tenant}
    return render(request, 'tenant.html',context)

def logout_user(request):
    logout(request)

    return redirect('core:index')


@login_required(login_url='core:index')
def add_property(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        location = request.POST['location']
        features = request.POST['features']
        image = request.FILES['image']

        try:
            property = Property.objects.create(name=name,address=address,location=location,features=features,image=image)
            property.save()
            messages.success(request,'Property added successfully')
            return redirect('core:home')
        except:
            messages.error(request,"Couldn't add property")
            return redirect('core:home')
    else:
        return redirect('core:home')
    
@login_required(login_url='core:index')    
def add_unit(request, id):
    property = Property.objects.filter(id=id).first()

    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']
        rent = request.POST['rent']
        features = request.POST['features']

        try:
            unit = Unit.objects.create(name=name,type=type,rent_cost=rent,features=features,property=property)
            unit.save()
            messages.success(request, 'Unit added Successfully !')
            return redirect('core:view_prop', prop=property.id)
        except:
            messages.error(request, "Couldn't add Unit !")
            return redirect('core:view_prop', prop=property.id)
    else:
        return redirect('core:view_prop', prop=property.id)
    
@login_required(login_url='core:index')
def allocate_tenant(request, unit, prop):

    unit_data = Unit.objects.filter(id=unit).first()
    property_data = Property.objects.filter(id=prop).first()
    context={'unit':unit_data,'property':property_data}

    if request.method == 'POST':
        name=request.POST['name']
        address=request.POST['address']
        rentdate=request.POST['rentdate']
        expirydate=request.POST['expirydate']
        document=request.FILES['document']
        
        try:
            tenant = Tenant.objects.create(name=name,unit=unit_data,address=address,monthly_rent_date=rentdate,lease_expiry_date=expirydate,document_proof=document)
            tenant.save()
            unit_data.is_available=False
            unit_data.save()
            messages.success(request,'Tenant allocated Successfully !')
            return redirect('core:tenant')
        except:
            messages.error(request,"Couldn't allocate tenant !")
            return render(request,'addtenant.html',context)


    else:
        return render(request,'addtenant.html',context)
        