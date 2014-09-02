from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import simplejson
from django.db.models.fields import DateField
from datetime import datetime
#from django.core import serializers
from pprint import pprint
import myapp.models

# Create your views here.

def index(request):
    model_list = myapp.models.load_models()
    context = {'model_list': model_list}
    return render(request, 'myapp/index.html', context)

### response additional data
def view(request, model):
    model_target = myapp.models.create_model(str(model).title(), app_label='myapp')
    model_list = myapp.models.load_models()
    current_model = model_list[model]
    fields = {}
    for val in current_model['fields']:
        fields[val['id']] = val
    current_model['fields'] = fields
    context = {
        'model_target': model_target,
        'model_list': model_list,
        'model_name': model,
        'model': current_model,
        'objects': model_target.objects.all()
    }
    return render(request, 'myapp/index.html', context)

### response json
def json(request, model):
    model_target = myapp.models.create_model(str(model).title(), app_label='myapp')
    model_list = myapp.models.load_models()
    objects = []
    for object in model_target.objects.all():
        objects.append(get_model_fields(object))
    current_model = model_list[model]
    fields = {}
    for val in current_model['fields']:
        fields[val['id']] = val
    current_model['fields'] = fields
    context = {
        'model_list': model_list,
        'model_name': model,
        'model': current_model,
        'objects': objects
    }
    data = simplejson.dumps(context)
    return HttpResponse(data, content_type='application/json')

### save data
def save(request, model):
    model_target = myapp.models.create_model(str(model).title(), app_label='myapp')
    try:
        b = model_target.objects.get(id=request.POST['pk'])
        setattr(b,request.POST['name'],request.POST['value'])
        b.save()
    except ObjectDoesNotExist:
        return HttpResponse('Error. Please try again later', status=400)
    except KeyError:
        return HttpResponse('Error. Please try again later', status=400)
    return HttpResponse('ok')

### create data
def create(request, model):
    model_target = myapp.models.create_model(str(model).title(), app_label='myapp')
    #try:
    b = model_target()
    for field in b._meta.fields:
        if type(field) is DateField:
            setattr(b, field.name, datetime.now())
    b.save()
    #except:
    #    return HttpResponse('Error. Please try again later', status=400)
    return HttpResponse('ok')

###
def get_model_fields(model):
    objects = {}
    for field in model._meta.fields:
        objects[field.name] = str(getattr(model, field.name))
        #if field.name != 'id':
        #    objects[field.name] = str(getattr(model, field.name))
        #else:
        #    objects['id'] = str(model.id)
    return objects
