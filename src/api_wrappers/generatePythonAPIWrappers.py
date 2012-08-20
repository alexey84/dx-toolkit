#!/usr/bin/env python

import os, sys, json, re

preamble = '''# Do not modify this file by hand.
#
# It is automatically generated by src/api_wrappers/generatePythonAPIWrappers.py.
# (Run make api_wrappers to update it.)

from dxpy import DXHTTPRequest
'''

class_method_template = '''
def {method_name}(input_params={{}}, **kwargs):
    return DXHTTPRequest('{route}', input_params, **kwargs)
'''

object_method_template = '''
def {method_name}(object_id, input_params={{}}, **kwargs):
    return DXHTTPRequest('/%s/{method_route}' % object_id, input_params, **kwargs)
'''

app_object_method_template = '''
def {method_name}(app_name_or_id, alias=None, input_params={{}}, **kwargs):
    fully_qualified_version = app_name_or_id + (('/' + alias) if alias else '')
    return DXHTTPRequest('/%s/{method_route}' % fully_qualified_version, input_params, **kwargs)
'''

print preamble

for method in json.loads(sys.stdin.read()):
    route, signature, opts = method
    method_name = signature.split("(")[0]
    if (opts['objectMethod']):
        root, oid_route, method_route = route.split("/")
        if oid_route == 'app-xxxx':
            print app_object_method_template.format(method_name=method_name, method_route=method_route)
        else:
            print object_method_template.format(method_name=method_name, method_route=method_route)
    else:
        print class_method_template.format(method_name=method_name, route=route)
