import json
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import PCConfiguration


def df(request):
    template_name = "components.html"

    return render(request, template_name)


@csrf_exempt
def buy(request):
    comp_spec = {}
    if request.method == 'POST':
        maindv = list(request.POST.dict().values())
        maindk = list(request.POST.dict().keys())
        comp = maindk[0] + maindv[0]
        res = json.loads(comp)
        pc_config = str(res['data'])
        if 'intelcorei9' in pc_config:
            comp_spec['processor'] = "Intel Core i9"
        elif 'intelcorei7' in pc_config:
            comp_spec['processor'] = "Intel Core i7"
        elif 'intelcorei5' in pc_config:
            comp_spec['processor'] = "Intel Core i5"

        if not ('intelcorei9' in pc_config or 'intelcorei7' in pc_config or 'intelcorei5' in pc_config):
            return HttpResponse("Please specify Processor.")

        if '16gbram' in pc_config:
            comp_spec['ram'] = "16GB RAM"
        elif '32gbram' in pc_config:
            comp_spec['ram'] = "32GB RAM"
        elif '64gbram' in pc_config:
            comp_spec['ram'] = "64GB RAM"

        if not ('16gbram' in pc_config or '32gbram' in pc_config or '64gbram' in pc_config):
            return HttpResponse("Please specify RAM.")

        if 'ssd512gb' in pc_config:
            comp_spec['hd'] = "SSD 512GB"
        elif 'ssd1tb' in pc_config:
            comp_spec['hd'] = "SSD 1TB"
        elif 'hdd512gb' in pc_config:
            comp_spec['hd'] = "HDD 512GB"
        elif 'hdd1tb' in pc_config:
            comp_spec['hd'] = "HDD 1TB"

        if not ('ssd512gb' in pc_config or 'ssd1tb' in pc_config or 'hdd512gb' in pc_config or 'hdd1tb' in pc_config):
            return HttpResponse("Please specify HDD.")

        if 'intel' in pc_config:
            comp_spec['graphics'] = "Intel Graphics"
        elif 'nvidia' in pc_config:
            comp_spec['graphics'] = "Nvidia Graphics"

        if not ('intel' in pc_config or 'nvidia' in pc_config):
            return HttpResponse("Please specify Graphics card.")

        # Fetch address
        if 'address' not in pc_config:
            return HttpResponse("Please specify Address.")

        print(comp_spec)
        # Save pc configuration to DB
        c = PCConfiguration(pc_config=comp_spec)
        c.save()

        subject = 'Computer Purchase Details'
        message = f"Processor: {c.processor}\nRAM: {c.ram}\nHDD: {c.hd}\nGraphics: {c.graphics}"
        from_email = 'alexjosepes123@gmail.com'
        recipient_list = ['alexkjoseakj23@gmail.com']

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return HttpResponse("Order placed.")
    else:
        return HttpResponse("Please verify the configuration.")
