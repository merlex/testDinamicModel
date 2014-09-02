from django.db import models
from django.contrib import admin
import yaml
import os
from pprint import pprint

# Create your models here.
def create_model(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model

def load_models():
    confDir = os.path.abspath(os.path.dirname(__file__))+'/'
    confFile = 'models.yaml'

    cfg = yaml.load(open(confDir+confFile))
    return cfg

def parse_model(name, val):
    fields = {}
    for fval in val['fields']:
        if fval['type'] == 'char':
            fields[fval['id']] = models.CharField(max_length=255,verbose_name=fval['title'])
        elif fval['type'] == 'date':
            fields[fval['id']] = models.DateField(verbose_name=fval['title'])
        elif fval['type'] == 'int':
            fields[fval['id']] = models.IntegerField(default=0,verbose_name=fval['title'])
        else:
            pass
    options = {
        'verbose_name': val['title'],
    }
    admin_opts = {} # An empty dictionary is equivalent to "class Admin: pass"
    return create_model(name.title(), fields,
        options=options,
        admin_opts=admin_opts,
        app_label='myapp',
        module='testwork.myapp.no_models',
    )

mymodels = load_models()
for key, val in mymodels.iteritems():
    #print key+', '+val['title']
    parse_model(key, val)