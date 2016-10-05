#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import codecs

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trimco.settings")

    if sys.argv[1] in 'popgr':
        from morphology.models import *

        '''
        rules = codecs.open('glossing_rules.txt', 'r','utf-8')
        for line in rules:
            line = line.replace('\t\t', '\t—\t')
            line = line.replace('\t\r', '\t—\r')
            line = line.replace('"', '')
            line = line.replace('\xa0', ' ')
            all_params = line.rstrip().split('\t')          
            [abbreviation, description, examples, abbr_overrides, section] = all_params[1:5]+[all_params[-1]]
            #rule = GlossingRule()
            #rule.populate(abbreviation, description, examples, abbr_overrides, section)
        '''
    else:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
