import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.Forms.YekaConnectionRegionForm import YekaConnectionRegionForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.models import YekaCompanyHistory, YekaConnectionRegion, ConnectionRegion
from ekabis.models.YekaCompany import YekaCompany
from ekabis.models.YekaPerson import YekaPerson
from ekabis.models.Employee import Employee
from ekabis.models.Yeka import Yeka
from ekabis.models.Company import Company
from ekabis.models.YekaPersonHistory import YekaPersonHistory
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaService
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType


@login_required
def return_yeka(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    parent_yekalar = Yeka.objects.filter(Q(isDeleted=False) & Q(yekaParent=None))
    companies = Company.objects.filter(isDeleted=False)
    try:
        with transaction.atomic():

            return render(request, 'Yeka/view_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '',
                           'parent_yekalar': parent_yekalar, 'companies': companies,
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_yeka(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    yeka_connection_form = YekaConnectionRegionForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':

                yeka_form = YekaForm(request.POST)
                yeka_connection_form = YekaConnectionRegionForm(request.POST)

                if yeka_form.is_valid() and yeka_connection_form.is_valid():
                    yeka = Yeka(definition=yeka_form.cleaned_data['definition'], date=yeka_form.cleaned_data['date'])
                    yeka.save()

                    total_capacity = 0
                    for region in yeka_connection_form.cleaned_data['connectionRegion']:
                        connection_region = ConnectionRegion.objects.get(uuid=region.uuid)
                        yeka_connection_region = YekaConnectionRegion(yeka=yeka, connectionRegion=connection_region)
                        yeka_connection_region.save()
                        total_capacity = total_capacity + region.value

                    yeka.capacity = total_capacity
                    yeka.unit = yeka_connection_form.cleaned_data['connectionRegion'][0].unit
                    yeka.save()

                    log = " Yeka eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka')

                else:
                    error_message_unit = get_error_messages(yeka_form)
                    yekafilter = {
                        'isDeleted': False,
                        'yekaParent': None
                    }
                    parent_yekalar = YekaService(request, yekafilter)
                    return render(request, 'Yeka/add_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'yeka_connection_form': yeka_connection_form})

            return render(request, 'Yeka/add_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'yeka_connection_form': yeka_connection_form})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                yekafilter = {
                    'uuid': uuid
                }
                obj = YekaService(request, yekafilter).first()
                parent = Yeka.objects.filter(Q(isDeleted=False) & Q(yekaParent__uuid=obj.uuid))
                if parent:
                    return JsonResponse({'status': 'Fail', 'msg': 'Yeka silinemez.Alt Yekalar bulunmaktadır.'})
                else:
                    obj.isDeleted = True
                    obj.save()
                    return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_yeka(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    yeka = Yeka.objects.get(uuid=uuid)
    yeka_form = YekaForm(request.POST or None, instance=yeka)
    alt_yekalar = Yeka.objects.filter(isDeleted=False, yekaParent__uuid=uuid)
    yeka_connections = YekaConnectionRegion.objects.filter(Q(isDeleted=False) & Q(yeka=yeka))

    try:
        with transaction.atomic():
            if request.method == 'POST':

                if yeka_form.is_valid():

                    yeka.definition = yeka_form.cleaned_data['definition']
                    yeka.date = yeka_form.cleaned_data['date']
                    yeka.save()

                    # regions = request.POST.getlist('region')
                    # current = []
                    # for region in yeka_connections:
                    #     current.append(region.connectionRegion.uuid)
                    #
                    # for region in regions:
                    #     if not current in region:
                    #         new = YekaConnectionRegion(yeka=yeka,
                    #                                    connectionRegion=ConnectionRegion.objects.get(uuid=region))

                    messages.success(request, 'Yeka Başarıyla Güncellendi')
                    return redirect('ekabis:view_yeka')
                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/change_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'yeka_connections': yeka_connections
                                   })

            return render(request, 'Yeka/change_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'yeka_connections': yeka_connections
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def alt_yeka_ekle(request, uuid):
    yeka_form = YekaForm()
    yeka = Yeka.objects.get(uuid=uuid)
    alt_yekalar = Yeka.objects.filter(yekaParent=yeka, isDeleted=False)

    try:
        with transaction.atomic():
            if request.method == 'POST':

                yeka_form = YekaForm(request.POST)

                if yeka_form.is_valid():

                    # form_capacity = int(yeka_form.cleaned_data['capacity'])
                    # total_capacity = 0
                    # if alt_yekalar:
                    #
                    #     for yeka in alt_yekalar:
                    #         total_capacity = total_capacity + yeka.capacity
                    #
                    # if yeka.capacity >= total_capacity + form_capacity:
                    new_yeka = Yeka(definition=yeka_form.cleaned_data['definition'],
                                        date=yeka_form.cleaned_data['date']
                                        )
                    new_yeka.save()
                    new_yeka.yekaParent = yeka
                    new_yeka.save()


                    log = "Alt Yeka eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka')

                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/add_sub_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'alt_yekalar': alt_yekalar
                                   })

            return render(request, 'Yeka/add_sub_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def yeka_person_list(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka = Yeka.objects.get(uuid=uuid)
    yeka_person = YekaPerson.objects.filter(Q(yeka=yeka) & Q(isDeleted=False))
    array = []
    for person in yeka_person:
        array.append(person.employee.uuid)
    persons = Employee.objects.filter(isDeleted=False).exclude(uuid__in=array)

    return render(request, 'Yeka/yekaPersonList.html',
                  {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid})


def yeka_person_assignment(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                person_uuid = request.POST['person_uuid']
                yeka_uuid = request.POST['yeka_uuid']

                yeka = Yeka.objects.get(uuid=yeka_uuid)
                person = Employee.objects.get(uuid=person_uuid)

                person_yeka = YekaPerson(yeka=yeka, employee=person, is_active=True)
                person_yeka.save()

                personHistory = YekaPersonHistory(yeka=yeka, person=person, is_active=True)
                personHistory.save()

                log = str(yeka.definition) + ' adlı yekaya - ' + str(
                    person.user.get_full_name()) + " adlı personel atandı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def yeka_person_remove(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                person = Employee.objects.get(uuid=uuid)

                yeka_person = YekaPerson.objects.get(Q(uuid=request.POST['yeka_uuid']) & Q(employee__uuid=uuid))

                yeka_person.isDeleted = True
                yeka_person.is_active = False
                yeka_person.save()

                personHistory = YekaPersonHistory(yeka=yeka_person.yeka, person=person, is_active=False)
                personHistory.save()

                log = str(yeka_person.yeka.definition) + ' adlı yekadan -' + str(
                    person.user.get_full_name()) + " personeli çıkarıldı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def yeka_company_list(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka = Yeka.objects.get(uuid=uuid)
    yeka_company = YekaCompany.objects.filter(Q(yeka=yeka) & Q(isDeleted=False))
    array = []
    for yeka in yeka_company:
        array.append(yeka.company.uuid)
    companies = Company.objects.filter(isDeleted=False).exclude(uuid__in=array)

    return render(request, 'Yeka/yeka_company_list.html',
                  {'companies': companies, 'yeka_companies': yeka_company, 'yeka_uuid': uuid})


def yeka_company_assignment(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                company_uuid = request.POST['company_uuid']
                yeka_uuid = request.POST['yeka_uuid']

                yeka = Yeka.objects.get(uuid=yeka_uuid)
                company = Company.objects.get(uuid=company_uuid)

                yeka_company = YekaCompany(yeka=yeka, company=company, is_active=True)
                yeka_company.save()

                log = str(yeka.definition) + ' adlı yekaya -' + str(company.name) + " adlı firma atandı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def yeka_company_remove(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                company = Company.objects.get(uuid=uuid)

                yeka_company = YekaCompany.objects.get(
                    Q(yeka__uuid=request.POST['yeka_uuid']) & Q(company__uuid=uuid) & Q(isDeleted=False))

                if yeka_company:
                    yeka_company.isDeleted = True
                    yeka_company.is_active = False
                    yeka_company.save()

                companyHistory = YekaCompanyHistory(yeka=yeka_company.yeka, company=company, is_active=False)
                companyHistory.save()

                log = str(yeka_company.yeka.definition) + '-' + str(
                    yeka_company.company.name) + " adlı firma çıkarıldı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
