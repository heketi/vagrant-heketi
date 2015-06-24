#!/usr/bin/env python

import httplib
import json
import string

conn = httplib.HTTPConnection('localhost:8080')
conn.request('GET', '/volumes')
r = conn.getresponse()
resp = json.loads(r.read())

for v in resp['volumes']:
    conn.request('DELETE', '/volumes/' + v['id'])
    r = conn.getresponse()
    print "%s -> %d" % (v['name'], r.status)
    d = r.read()

