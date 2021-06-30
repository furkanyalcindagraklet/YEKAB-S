import traceback

from django.contrib.auth.models import User, Group
from django.db.models import Q

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.Claim import Claim
from ekabis.models.Communication import Communication
from ekabis.models.Company import Company
from ekabis.models.DirectoryCommission import DirectoryCommission
from ekabis.models.DirectoryMember import DirectoryMember
from ekabis.models.DirectoryMemberRole import DirectoryMemberRole
from ekabis.models.Employee import Employee
from ekabis.models.Logs import Logs
from ekabis.models.Menu import Menu
from ekabis.models.MenuAdmin import MenuAdmin
from ekabis.models.MenuDirectory import MenuDirectory
from ekabis.models.MenuPersonel import MenuPersonel
from ekabis.models.Notification import Notification
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Person import Person
from ekabis.models.Settings import Settings


def UserService(request,filter):
    try:
        if filter:
            if type(filter) !=type(Q()):
               return User.objects.filter(**filter)
            else:
                return User.objects.filter(filter)
        else:
            return User.objects.all()
    except User.DoesNotExist:
        return None
    except Exception as e:
        print(e)
        pass
    traceback.print_exception()

def GroupService(request, filter):
    try:
        if filter:
            return Group.objects.filter(**filter)
        else:
            return Group.objects.all()
    except Group.DoesNotExist:
        return None
    except Exception as e:
        print(e)
        pass
    traceback.print_exception()

def PersonService(request, filter):
    try:
        if filter:
            return Person.objects.filter(**filter)
        else:
            return Person.objects.all()
    # except Person.DoesNotExist:
    #     return None
    except Exception as e:
        print(e)
        pass
    traceback.print_exception()
def CommunicationService(request, filter):
    try:
        if filter:
            return Communication.objects.filter(**filter)
        else:
            return Communication.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()

def CategoryItemService(request, filter):
    try:
        if filter:
            return CategoryItem.objects.filter(**filter)
        else:
            return CategoryItem.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def CompanyService(request, filter):
    try:
        if filter:
            return Company.objects.filter(**filter)
        else:
            return Company.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def DirectoryMemberService(request, filter):
    try:
        if filter:
            if type(filter)!=type(Q()):
                return DirectoryMember.objects.filter(**filter)
            else:
                return DirectoryMember.objects.filter(filter)
        else:
            return DirectoryMember.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def DirectoryCommissionService(request, filter):
    try:
        if filter:
            return DirectoryCommission.objects.filter(**filter)
        else:
            return DirectoryCommission.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def DirectoryMemberRoleService(request, filter):
    try:
        if filter:
            return DirectoryMemberRole.objects.filter(**filter)
        else:
            return DirectoryMemberRole.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def EmployeeService(request, filter):
    try:
        if filter:
            if type(filter) != type (Q()):
                return Employee.objects.filter(**filter)
            else:
                Employee.objects.filter(filter)
        else:
            return Employee.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def LogsService(request, filter):
    try:
        if filter:
            if type(filter) !=type(Q()):
                return Logs.objects.filter(**filter)
            else:
                return Logs.objects.filter(filter)
        else:
            return Logs.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def MenuService(request, filter):
    try:
        if filter:
            return Menu.objects.filter(**filter)
        else:
            return Menu.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def MenuAdminService(request, filter):
    try:
        if filter:
            return MenuAdmin.objects.filter(**filter).order_by("sorting")
        else:
            return MenuAdmin.objects.all().order_by("sorting")
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def MenuDirectoryService(request, filter):
    try:
        if filter:
            return MenuDirectory.objects.filter(**filter).order_by("sorting")
        else:
            return MenuDirectory.objects.all().order_by("sorting")
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def MenuPersonelService(request, filter):
    try:
        if filter:
            return MenuPersonel.objects.filter(**filter).order_by("sorting")
        else:
            return MenuPersonel.objects.all().order_by("sorting")
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def NotificationService(request, filter):
    try:
        if filter:
            return Notification.objects.filter(**filter)
        else:
            return Notification.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def ActiveGroupService(request, filter):
    try:
        if filter:
            return ActiveGroup.objects.filter(**filter)
        else:
            return ActiveGroup.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()
def PermissionService(request, filter):
    try:
        if filter:
            return Permission.objects.filter(**filter)
        else:
            return Permission.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()


def ClaimService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Claim.objects.filter(**filter)
            else:
                return Claim.objects.filter(filter)
        else:
            return Claim.objects.all()
    except Exception as e:
            print(e)
            pass
    traceback.print_exception()


def PermissionGroupService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return PermissionGroup.objects.filter(**filter)
            else:
                return PermissionGroup.objects.filter(filter)
        else:
            return PermissionGroup.objects.all()
    except Exception as e:
            traceback.print_exception()
def SettingsService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Settings.objects.filter(**filter)
            else:
                return Settings.objects.filter(filter)
        else:
            return Settings.objects.all()
    except Exception as e:
            traceback.print_exception()