from rest_framework import exceptions
from rest_framework.throttling import BaseThrottle
#from api.models import Users
from utils.md5 import Md5
import os

data = {}

class VisitThrottle(BaseThrottle):
    def allow_request(self, request, view):
        if request.method == "GET":
            if os.path.exists('/data/pi/tracking.pid'):
                print(1)
                return False
            else:
                print(2)
                return True

        elif request.method == "POST":
            return True
        elif request.method == "PATCH":
            return True
        elif request.method == "DELETE":
            return True

    def wait(self):
        # ctime = datetime.datetime.now()
        # wait_time = (ctime - data["visit_check"]).seconds
        # balance_time = 1 - wait_time
        return 1
