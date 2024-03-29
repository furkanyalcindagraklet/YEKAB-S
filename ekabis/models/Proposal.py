from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.Coordinate import Coordinate
from ekabis.models.Location import Location
from ekabis.models.Proposalnstitution import ProposalInstitution

#Aday Yeka yekanın lokasyonun da öneri
class Proposal(BaseModel):
    capacity = models.IntegerField(blank=True, null=True)
    information_form=models.FileField(null=True,blank=True)
    date=models.DateField(null=True, blank=True)
    coordinate=models.ManyToManyField(Coordinate)
    location=models.ManyToManyField(Location)
    farm_form=models.FileField(null=True,blank=True)
    status=models.BooleanField(default=False)
    name = models.TextField(blank=False, null=False, verbose_name='Aday Yeka')
    # Kurum önerileri
    institution=models.ManyToManyField(ProposalInstitution)

