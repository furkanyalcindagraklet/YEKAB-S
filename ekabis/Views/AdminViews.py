from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ekabis.Forms.DisabledUserForm import DisabledUserForm
from ekabis.services import general_methods
from ekabis.models import  DirectoryMember,Employee
from ekabis.services.services import PersonService,UserService,GroupService,CategoryItemService,DirectoryCommissionService,DirectoryMemberRoleService,CommunicationService

@login_required
def updateProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user=request.user
    user_form = DisabledUserForm(request.POST or None, instance=request.user)
    password_form = SetPasswordForm(request.user, request.POST)
    if request.method == 'POST':
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            log = str(user.get_full_name()) + " admin sifre guncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('ekabis:admin-profil-guncelle')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'admin/admin-profil-guncelle.html',
                  {'user_form': user_form, 'password_form': password_form})


@login_required
def activeGroup(request, pk):
    gropfilter={
        'name' : request.GET.get('group')
    }
    group = GroupService(request,gropfilter).exists()
    pk = request.GET.get('pk')

    communicationfilter={
        'pk' : request.GET.get('communication')
    }
    communication = CommunicationService(request,communicationfilter)[0]
    personfilter={
        'pk' : request.GET.get('person')
    }
    person = PersonService(request,personfilter)[0]
    userfilter={
        'pk' : request.GET.get('user')
    }
    user = UserService(request,userfilter)[0]
    if group.name == "Admin":
        user.groups.add(group)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return redirect('ekabis:view_admin')
    elif group.name == "Personel":
        employe = Employee(person=person,
                                 communication=communication, user=user,workDefinition=CategoryItemService(request,None))
        employe.save()
        user.groups.add(group)
        user.save()
        return redirect('ekabis:view_personel', pk=employe.pk)

    elif group.name == "Yonetim":
        member = DirectoryMember(person=person, communication=communication, user=user,
                                 role=DirectoryMemberRoleService(request,None)[0],
                                 commission=DirectoryCommissionService(request,None)[0])
        member.save()
        user.groups.add(group)
        user.save()
        return redirect('ekabis:view_directoryMember', pk=member.pk)
    return {}
