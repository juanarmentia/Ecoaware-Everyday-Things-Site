# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from ecoaware.devices.utils.getViewCoffees import get_numcoffees_by_date, get_coffees_by_date
from ecoaware.devices.utils.getViewEnergy import get_energy_by_group

from .forms import DevicesForm, UserCreateForm, CustomUserForm, RfidForm, CustomUserUpdateForm, UserUpdateForm, User_QuestionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Device, CustomUser, TagRFID, Question, User_Question

from django.views.generic.edit import UpdateView

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm

#New device creation form
@login_required(login_url='/signin')
def newDevice(request):
    if request.method=='POST':
        form = DevicesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../privatehome')
    else:
        form = DevicesForm()
    return render_to_response('newdevice.html', {'form':form}, context_instance=RequestContext(request))

#New device creation form
@login_required(login_url='/signin')
def listDevices(request):
    allDevices = Device.objects.all()
    return render_to_response('listdevices.html', {'devices':allDevices}, context_instance=RequestContext(request))

@login_required(login_url='/signin')
def updateDevice(request,username):
    d = Device.objects.get(username__exact=username)
    if request.method=='POST':
        form = DevicesForm(request.POST, instance = d)
        print d
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../list')
    if request.method == 'GET':
        form = DevicesForm(instance=d)

    return render_to_response('updatedevice.html', {'form':form, 'Device':d}, context_instance=RequestContext(request))
    


#New user creation view
def newUser(request, tagrfid):
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.method == 'POST' and 'fulluser_form' in request.POST:
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserCreateForm(data=request.POST)
        customUser_form = CustomUserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and customUser_form.is_valid():

            # Save the user's form data to the database.
            user = user_form.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = customUser_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()
            
            #ACTIVAR EL CAMPO DEL RFID
            tagToUpdate  = TagRFID.objects.get(rfid__exact=request.POST['rfid'])
            tagToUpdate.active = 1
            tagToUpdate.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, customUser_form.errors

    elif request.method == 'POST':
        user_form = UserCreateForm()
        customUser_form = CustomUserForm({'rfid':tagrfid})
        id_question1 = 39
        id_question2 = id_question1+1
        answer1 = int(request.POST['answer1'])
        answer2 = int(request.POST['answer2'])
        if User_Question.objects.filter(rfid=tagrfid, question=id_question1).count()!=0:
            userQuestion1 = User_Question.objects.get(rfid=tagrfid, question=id_question1)
            userQuestion1.answer = answer1
            userQuestion1.save()
        else:
            userQuestion1 = User_QuestionForm({'rfid':tagrfid, 'question':id_question1, 'answer':answer1})
            userQuestion1.save()
        if User_Question.objects.filter(rfid=tagrfid, question=id_question2).count()!=0:
            userQuestion2 = User_Question.objects.get(rfid=tagrfid, question=id_question2)
            userQuestion2.answer = answer2
            userQuestion2.save()
        else:
            userQuestion2 = User_QuestionForm({'rfid':tagrfid, 'question':id_question2, 'answer':answer2})
            userQuestion2.save()
    else:
        user_form = UserCreateForm()
        customUser_form = CustomUserForm({'rfid':tagrfid})

    # Render the template depending on the context.
    return render_to_response('newuser.html', {'user_form': user_form, 'customUser_form': customUser_form, 'registered': registered, 'rfid':tagrfid}, context)


#Update user information
@login_required(login_url='/signin')
def updateUser(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserUpdateForm(data=request.POST)
        customUser_form = CustomUserUpdateForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and customUser_form.is_valid():
            # Save the user's form data to the database.
            currentUser = User.objects.get(username__exact=request.user.username)
            currentUser.email = request.POST['email']
            user = currentUser.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            currentCustomUser = CustomUser.objects.get(user_id__exact=currentUser.id)
            currentCustomUser.twitter = request.POST['twitter']
            profile = currentCustomUser.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, customUser_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        currentUser = User.objects.get(username__exact=request.user.username)
        currentCustomUser = CustomUser.objects.get(user_id__exact=currentUser.id)
        user_form = UserUpdateForm({'email':currentUser.email})
        customUser_form = CustomUserUpdateForm({'twitter':currentCustomUser.twitter})
        

    # Render the template depending on the context.
    return render_to_response('updateuser.html', {'user_form': user_form, 'customUser_form': customUser_form, 'registered': registered}, context)


#Login view
def sign_in(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/privatehome')
    signin_form = AuthenticationForm()
    signup_form = RfidForm()
    if request.method=='POST' and 'signin' in request.POST:
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            user = request.POST['username']
            passw = request.POST['password']
            access = authenticate(username=user, password=passw)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return HttpResponseRedirect('/privatehome')
                else:
                    return render_to_response('noactive.html', context_instance=RequestContext(request))
            else:
                return render_to_response('noexist.html', context_instance=RequestContext(request))
        else:
            print "is not valid form"
    elif request.method=='POST' and 'signup' in request.POST:
        signup_form = RfidForm(data=request.POST)
        #if signup_form.is_valid():
        tagrfid = request.POST['rfid']
        #cd = signup_form.cleaned_data
        #print cd['rfid']
        if TagRFID.objects.filter(rfid=tagrfid).count()!=0:
            if TagRFID.objects.filter(rfid=tagrfid, active=0).count()!=0:
                #return HttpResponseRedirect('/user/new/'+tagrfid)
                return HttpResponseRedirect('/'+tagrfid+'/questionnaire/1/1')
        elif tagrfid!='':
            signin_form = AuthenticationForm()
            signup_form = RfidForm({'rfid':tagrfid})
            norfid = True
            return render_to_response('signin.html', {'signin_form':signin_form, 'signup_form':signup_form, 'norfid':norfid}, context_instance=RequestContext(request))
    else:
        signin_form = AuthenticationForm()
        signup_form = RfidForm()
    return render_to_response('signin.html', {'signin_form':signin_form, 'signup_form':signup_form}, context_instance=RequestContext(request))
 

#Panel view, both for admin and ordinary users
@login_required(login_url='/signin')
def privatehome(request):
    usuario = request.user
    if usuario.is_superuser:
        return render_to_response('privateadmin.html', {'usuario':usuario}, context_instance=RequestContext(request))
    else:
        return render_to_response('private.html', {'usuario':usuario}, context_instance=RequestContext(request))


#Closing session
@login_required(login_url='/signin')
def closesession(request):
    logout(request)
    return HttpResponseRedirect('/signin')


@login_required(login_url='/signin')
def coffeeschart(request,ndays,device):
    nDays = int(ndays)
    currentUser = request.user
    if currentUser.username=='admin':
        admin = True
    else:
        admin = False
    if currentUser.is_superuser:
        deviceName = device
    else:
        currentCustomUser = CustomUser.objects.get(user_id__exact=currentUser.id)
        customTagRfid = TagRFID.objects.get(rfid__exact=currentCustomUser.rfid)
        deviceName = customTagRfid.device_id
    nCoffees = get_numcoffees_by_date(deviceName, nDays)
    return render_to_response('coffeesbarplot.html', {'nCoffees':nCoffees, 'superuser':admin, 'device':deviceName}, context_instance=RequestContext(request))


@login_required(login_url='/signin')
def energychart(request,ndays,device):
    nDays = int(ndays)
    currentUser = request.user
    if currentUser.username=='admin':
        admin = True
    else:
        admin = False
    if currentUser.is_superuser:
        deviceName = device
    else:
        currentCustomUser = CustomUser.objects.get(user_id__exact=currentUser.id)
        customTagRfid = TagRFID.objects.get(rfid__exact=currentCustomUser.rfid)
        deviceName = customTagRfid.device_id
    accEnergy = get_energy_by_group(deviceName, nDays)
    return render_to_response('energybarplot.html', {'accEnergy':accEnergy, 'superuser':admin, 'device':deviceName}, context_instance=RequestContext(request))


@login_required(login_url='/signin')
def scatterchart(request,nhours,ndays,device):
    nDays = int(ndays)
    nHours = int(nhours)
    rangeDays = []
    for i in range(1,nDays+1):
        rangeDays.append(i)
    currentUser = request.user
    if currentUser.username=='admin':
        admin = True
    else:
        admin = False
    if currentUser.is_superuser:
        deviceName = device
    else:
        currentCustomUser = CustomUser.objects.get(user_id__exact=currentUser.id)
        customTagRfid = TagRFID.objects.get(rfid__exact=currentCustomUser.rfid)
        deviceName = customTagRfid.device_id
    coffees = get_coffees_by_date(deviceName, nDays, nHours)
    if nHours==12:
        return render_to_response('coffeesscatterplot12.html', {'coffees':coffees[0], 'rangedays':rangeDays, 'startdate':coffees[2], 'finishdate':coffees[1], 'superuser':admin, 'device':deviceName}, context_instance=RequestContext(request))
    else:
        return render_to_response('coffeesscatterplot24.html', {'coffees':coffees[0], 'rangedays':rangeDays, 'startdate':coffees[2], 'finishdate':coffees[1], 'superuser':admin, 'device':deviceName}, context_instance=RequestContext(request))


@login_required(login_url='/signin')
def graphics(request):
    if request.method=='POST' and 'graphic' in request.POST:
        device = Device.objects.get(name__exact=request.POST['devices'])
        #print request.POST['graphic']
        #print device.username
        return HttpResponseRedirect('../'+device.username+'/'+request.POST['graphic'])
    usuario = request.user
    if usuario.is_superuser:
        allDevices = Device.objects.all()
        return render_to_response('graphicsmenuadmin.html', {'usuario':usuario, 'devices':allDevices}, context_instance=RequestContext(request))
    else:
        return render_to_response('graphicsmenu.html', {'usuario':usuario}, context_instance=RequestContext(request))
    

def resetpassword(request):
    if request.method == 'POST':
        return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, 'forgot_password.html')


def questionnaire(request, rfid, module, question):
    if request.method=='POST':
        if module == '1':
            id_question = int(question)-1
        elif module == '2':
            if question == '1':
               id_question = 4
            else:
                id_question1 = (int(question) + 4 + (int(question)-1)) - 2
                id_question2 = id_question1+1
        elif module == '3':
            id_question1 = (int(question) + 16 + (int(question)-1)) - 2
            id_question2 = id_question1+1
        elif module == '4':
            id_question1 = (int(question) + 28 + (int(question)-1)) - 2
            id_question2 = id_question1+1
        else:
            id_question = 0
        if (module == '2' and question != '1') or module == '3' or module == '4':
            answer1 = int(request.POST['answer1'])
            answer2 = int(request.POST['answer2'])
            if User_Question.objects.filter(rfid=rfid, question=id_question1).count()!=0:
                userQuestion1 = User_Question.objects.get(rfid=rfid, question=id_question1)
                userQuestion1.answer = answer1
                userQuestion1.save()
            else:
                userQuestion1 = User_QuestionForm({'rfid':rfid, 'question':id_question1, 'answer':answer1})
                userQuestion1.save()
            if User_Question.objects.filter(rfid=rfid, question=id_question2).count()!=0:
                userQuestion2 = User_Question.objects.get(rfid=rfid, question=id_question2)
                userQuestion2.answer = answer2
                userQuestion2.save()
            else:
                userQuestion2 = User_QuestionForm({'rfid':rfid, 'question':id_question2, 'answer':answer2})
                userQuestion2.save()
        else:
            answer = int(request.POST['answer'])
            if User_Question.objects.filter(rfid=rfid, question=id_question).count()!=0:
                userQuestion = User_Question.objects.get(rfid=rfid, question=id_question)
                userQuestion.answer = answer
                userQuestion.save()
            else:
                userQuestion = User_QuestionForm({'rfid':rfid, 'question':id_question, 'answer':answer})
                userQuestion.save()
                
    return render_to_response('questionnaire/cuestionario-'+module+'_'+question+'.html', {'rfid':rfid}, context_instance=RequestContext(request))









