from django.db import models

from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class YekaCompany(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(null=True,blank=True)

    def __str__(self):
        return '%s ' % self.company.name
