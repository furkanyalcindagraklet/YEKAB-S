import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ekabis.Forms.ExtraTimeForm import ExtraTimeForm
from ekabis.models.ExtraTime import ExtraTime
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import ExtraTimeService, ExtraTimeGetService


@login_required
def return_add_extra_time(request, yeka, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yeka = Yeka.objects.get(uuid=yeka)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)

        # if ExtraTime.objects.filter(yekabusinessblog=yekabussinessblog):
        #      return redirect('ekabis:change_extratime', ExtraTime.objects.get(yekabusinessblog=yekabussinessblog).uuid)
        extratime_form = ExtraTimeForm()
        extra_times= ExtraTime.objects.filter(yekabusinessblog=yekabussinessblog)
        with transaction.atomic():
            if request.method == 'POST':
                extratime_form = ExtraTimeForm(request.POST)
                if extratime_form.is_valid():
                    time = extratime_form.save(commit=False)
                    time.user = request.user
                    time.yekabusinessblog = yekabussinessblog
                    time.yeka = yeka
                    time.save()
                    messages.success(request, 'Ek Süre Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yekabusinessBlog', yeka.uuid)
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/add_extratime.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'ExtraTime/add_extratime.html',
                          {'extratime_form': extratime_form,
                           'yeka': yeka,'extra_times':extra_times,
                           'yekabussinessblog': yekabussinessblog
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusinessBlog', yeka.uuid)


@login_required
def return_list_extra_time(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    ExtraTimefilter = {
        'isDeleted': False

    }
    ekstratime = ExtraTimeService(request,None)
    return render(request, 'ExtraTime/view_extratime.html',
                  {'ekstratime': ekstratime})

@login_required
def return_update_extra_time(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    extra_time_filter={
        'uuid':uuid
    }
    extratime = ExtraTimeGetService(request,extra_time_filter)
    extratime_form = ExtraTimeForm(request.POST or None, instance=extratime)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                if extratime_form.is_valid():
                    extratime_form.save()
                    messages.success(request, 'Ek Süre Güncellenmiştir')
                    return redirect('ekabis:view_yekabusinessBlog', extratime.yeka.uuid)
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/change_extratime.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'ExtraTime/change_extratime.html',
                          {'extratime_form': extratime_form, })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_extra_time(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                extra_time_filter = {
                    'uuid': uuid
                }
                obj = ExtraTimeGetService(request,extra_time_filter)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
