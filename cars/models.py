from django.db import models


class Parking(models.Model):
    reg_number = models.CharField(max_length=200)
    colour = models.CharField(max_length=200)
    slot = models.IntegerField()
    in_use = models.IntegerField()
    reg_date = models.DateTimeField('date published')
    slot_used = models.IntegerField(default=0)

    def invalid_slot(self):
        if self.slot_used == 1 and self.in_use ==1: 
            return(0)
        else:
            return(1)
        