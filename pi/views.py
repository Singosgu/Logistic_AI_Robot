from rest_framework.views import APIView
from rest_framework.response import Response
from utils.fbmsg import FBMsg
from utils import mac_address
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import os
from django.shortcuts import render

def index(request):
    context = {}
    ip = request.get_host()
    print(ip)
    context['mac'] = mac_address.get_mac_address()
    return render(request, 'index.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class MoveAPI(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        os.system("python3 /data/pi/utils/tracking.py")
        ret = FBMsg.ret()
        ret['ip'] = ip
        return Response(ret)
