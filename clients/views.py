from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Client, Gender, Civilstat, Product, Clientaccountcode, Membertype, Clientstat
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime

@login_required(login_url= '/users/login')
def index(request):
    #user_list = User.objects.order_by('-id')[:5]
    #context = {'user_list': user_list}
    #return render(request, 'users/index.html', context)
    client_list = Client.objects.all().order_by('-id')
    paginator = Paginator(client_list, 5)    
    page_number = request.GET.get('page')
    client_list = paginator.get_page(page_number)

    return render (request, 'clients/index.html', {'page_obj': client_list})

@login_required(login_url= '/users/login')
def search(request):
    term = request.GET.get('search', '')
    client_list = Client.objects.filter(Q(client_fname__icontains=term) | Q(client_lname__icontains=term)).order_by('-id')
    paginator = Paginator(client_list, 5)    
    page_number = request.GET.get('page')
    client_list = paginator.get_page(page_number)
    return render (request, 'clients/index.html', {'page_obj': client_list})

@login_required(login_url= '/users/login')
def addclient(request):
    genders = Gender.objects.only('genders')
    cstatus = Civilstat.objects.all().values('civil_status')
    branches = Clientaccountcode.objects.only('branch')

    user = request.user
    if user.can_selectbranch==False:
        branches = user.user_branch

    membertypes = Membertype.objects.only('membertypes')
    client_status = Clientstat.objects.only('client_status')

    context = {'genders': genders, 
                'cstatus': cstatus, 
                'branches': branches, 
                'membertypes': membertypes, 
                'client_status': client_status}
    return render(request, 'clients/add.html',  context)


def processaddclient(request):
    client_fname                = request.POST.get('client_fname')
    client_mname                = request.POST.get('client_mname')
    client_lname                = request.POST.get('client_lname')
    client_email                = request.POST.get('client_email')
    client_status               = request.POST.get('client_status')
    client_address              = request.POST.get('client_address')
    client_dob                  = request.POST.get('client_dob')
    client_gender               = request.POST.get('client_gender')
    client_cstatus              = request.POST.get('client_cstatus')
    client_spouse               = request.POST.get('client_spouse')
    client_children             = request.POST.get('client_children') 
    client_membertype           = request.POST.get('membership_type') 
    client_celnumber            = request.POST.get('client_celnumber')
    client_branch               = request.POST.get('client_branch')
    client_occupation           = request.POST.get('client_occupation')

    # getclientcodes=get_object_or_404(Clientaccountcode, branch=client_branch)
    
    getclientcodes              = Clientaccountcode.objects.get(branch=client_branch)
    client_zipcode              = getclientcodes.zipcode
    client_branchcode           = getclientcodes.branchcode

    getbranchcount = Client.objects.filter(client_branchcode=client_branchcode)
    
    branchcodecounts=1

    if getbranchcount:
        for getcounts in getbranchcount:
            branchcodecounts+=1   

    client_code         =           str(client_branchcode) + str(client_zipcode) + str(branchcodecounts)
    
    reg_date = request.POST.get('reg_date')   

    if request.FILES.get('client_image'):
        client_image = request.FILES.get('client_image')
    else:
        client_image='profile_pic/default_image.png'

    
    client = Client.objects.create(client_fname=client_fname, client_mname=client_mname, client_lname=client_lname, 
                                    client_email=client_email, client_status=client_status, client_address=client_address, 
                                    client_dob=client_dob, client_gender=client_gender, client_cstatus=client_cstatus,
                                    client_spouse=client_spouse, client_children=client_children, client_membertype=client_membertype, 
                                    client_celnumber=client_celnumber, client_branch=client_branch, client_occupation=client_occupation, 
                                    client_image=client_image, reg_date=reg_date, client_zipcode=client_zipcode,
                                     client_branchcode=client_branchcode, client_code=client_code)
        
    client.save()
    return HttpResponseRedirect('/clients')
    #try:
    #    n=User.objects.get(user_email=email)
        #if email already exist
    #    return render(request, 'clients/add.html', { 
    #        'error_message': "Duplicated Email: " + client_email, 'client_fname': client_fname, 'client_lname': client_lname, 'client_email': client_email, 'client_status': client_status
    #        })
    #except ObjectDoesNotExist:

@login_required(login_url= '/users/login')
def clientdetail(request, profile_id):
    try:
        client = Client.objects.get(pk=profile_id)
        clientAge = int((datetime.now().date() - client.client_dob).days / 365.25)        
    except Client.DoesNotExist:
        raise Http404("Profile does not exist")
    return render(request, 'clients/detail.html', {'client': client, 'clientAge': clientAge})

@login_required(login_url= '/users/login')
def clientdelete(request, profile_id):
    Client.objects.filter(id=profile_id).delete()
    return HttpResponseRedirect('/clients')

@login_required(login_url= '/users/login')
def clientedit(request, profile_id):
    genders = Gender.objects.only('genders')
    cstatus = Civilstat.objects.all().values('civil_status')
    branches = Clientaccountcode.objects.only('branch')
    membertypes = Membertype.objects.only('membertypes')
    client_status = Clientstat.objects.only('client_status')
    try:
        client = Client.objects.get(pk=profile_id)        
    except Client.DoesNotExist:
        raise Http404("Profile does not exist")

    context = {'genders': genders, 
                    'cstatus': cstatus, 
                    'branches': branches, 
                    'membertypes': membertypes,
                    'client_status': client_status, 
                    'client': client}     

    return render(request, 'clients/edit.html', context)

def processclientedit(request, profile_id):
    client=get_object_or_404(Client, pk=profile_id)
    client_pic=request.FILES.get('client_image')
    try:
        client_fname = request.POST.get('client_fname')
        client_mname = request.POST.get('client_mname')
        client_lname = request.POST.get('client_lname')
        client_email = request.POST.get('client_email')
        client_status = request.POST.get('client_status')
        client_address = request.POST.get('client_address')
        client_dob = request.POST.get('client_dob')
        client_gender = request.POST.get('client_gender')
        client_cstatus = request.POST.get('client_cstatus')
        client_spouse = request.POST.get('client_spouse')
        client_children = request.POST.get('client_children')
        client_membertype = request.POST.get('membership_type')
        client_celnumber = request.POST.get('client_celnumber')
        client_branch = request.POST.get('client_branch')
        client_occupation = request.POST.get('client_occupation')

    except(KeyError, Client.DoesNotExist):
        return render(request, 'clients/detail.html', {
            'client': client,
            'error_message': "Problem updating record",
        })
    else:
        client_profile = Client.objects.get(id=profile_id)
        client_profile.client_fname=client_fname
        client_profile.client_mname=client_mname
        client_profile.client_lname=client_lname
        client_profile.client_email=client_email
        client_profile.client_status=client_status
        client_profile.client_address=client_address
        client_profile.client_dob=client_dob
        client_profile.client_gender=client_gender
        client_profile.client_cstatus=client_cstatus
        client_profile.client_spouse=client_spouse
        client_profile.client_children=client_children
        client_profile.client_membertype=client_membertype
        client_profile.client_celnumber=client_celnumber
        client_profile.client_branch=client_branch
        client_profile.client_occupation=client_occupation
        
        if client_pic:
            client_profile.client_image=client_pic
        client_profile.save()
        return HttpResponseRedirect(reverse('clients:clientdetail', args=(profile_id,)))
