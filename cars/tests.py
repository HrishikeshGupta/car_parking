import datetime

from django.test import TestCase

from .models import Parking


class ParkingModelTests(TestCase):
    def slot_used_for_occupied_slot(self):
        parking_obj = Parking.objects.fiter(in_use=1, slot_used=0).limit(1)
        self.assertIs(parking_obj.invalid_slot(), 1)

        
        
if __name__ == '__main__':
    unittest.main()