#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
from operator import itemgetter

from settings import BASEURL, DIR, HTML_FIELDS
import utils

def get_metadata(assembly_id, range=(None, None)):
    with open('%s/%d.csv' % (DIR['meta'], assembly_id), 'r') as f:
        data = []
        for row in f.readlines():
            items = [item.strip('"') for item in row.decode('utf-8').split(',')]
            data.append(itemgetter(0,3,8)(items))

    meta = {}
    for d in data:
        meta[d[0]] = (d[1], d[2])

    return meta

def get_page(assembly_id, bill_id, link_id, field):
    url = '%s%s' % (BASEURL[field], link_id)
    outp = '%s/%s/%s.html' % (DIR[field], assembly_id, bill_id)

    if not os.path.isfile(outp):
        is_first = True
        while is_first or 'TEXTAREA ID="MSG" STYLE="display:none"' in doc:
            r = urllib2.urlopen(url)
            doc = r.read()
            is_first = False

        with open(outp, 'w') as f:
            f.write(doc)

def get_specifics(assembly_id, bill_id, link_id):
    if assembly_id > 16:
        baseurl = BASEURL['specifics']
    else:
        baseurl = BASEURL['specifics_old']

    outp = '%s/%s/%s.html' % (DIR['specifics'], assembly_id, bill_id)
    if not os.path.isfile(outp):
        url = '%s%s' % (baseurl, link_id)
        utils.get_webpage(url, outp)

def get_summaries(assembly_id, bill_id, link_id, has_summaries):
    if has_summaries==1:
        outp = '%s/%s/%s.html' % (DIR['summaries'], assembly_id, bill_id)
        if not os.path.isfile(outp):
            utils.get_webpage('%s%s' % (BASEURL['summaries'], link_id), outp)

def get_html(assembly_id, range=(None, None)):
    for field in HTML_FIELDS:
        utils.check_dir('%s/%s' % (DIR[field], assembly_id))

    metadata = get_metadata(assembly_id, range=range)

    for bill_id in metadata:
        link_id, has_summaries = metadata[bill_id]
        for field in HTML_FIELDS[1:3]:
            get_page(assembly_id, bill_id, link_id, field)
        get_specifics(assembly_id, bill_id, link_id)
        get_summaries(assembly_id, bill_id, link_id, has_summaries)

        sys.stdout.write('%s\t' % bill_id)
        sys.stdout.flush()
