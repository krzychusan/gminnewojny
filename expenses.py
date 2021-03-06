#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbf
import gminy
import par_mapper
import cities
import pickle
import os

FILE_PICKLE = 'data/data_pickle.x'

PLANNED_EXPENSE = 0
EXECUTED_EXPENSE = 1

def generate_expenditures():
    table = dbf.Table('data/Rb28s.dbf')
    table.open()

    par_data = par_mapper.get_par('data/par_input.txt')
    rozdzial_data = par_mapper.get_par('data/rozdzial_input.txt')
    gminy_data = gminy.getGminy(gminy.WORKBOOK)

    result = {}

    for record in table:
        wk_pk_gk = gminy.WkPkGkToStr(record['wk'], record['pk'], record['gk'])
        
        try:
            gminy_record = gminy_data[wk_pk_gk]
            par_record = par_data[int(record['par'])]
            rozdzial   = rozdzial_data[int(record['rozdzial'])]
        except KeyError:
            continue

        planned = record['r1']
        executed = record['r4']
        
        gmina_type = gminy_record[2]
        gmina_name = gminy_record[1]
        gmina_key = gminy_record[0]
        
        if gmina_key not in result:
            result[gmina_key] = {}
        
        expense_data = par_record
        if expense_data not in result[gmina_key]:
            result[gmina_key][expense_data] = {}
        
        if rozdzial not in result[gmina_key][expense_data]:    
            result[gmina_key][expense_data][rozdzial] = [0.0, 0.0]
            
        result[gmina_key][expense_data][rozdzial][PLANNED_EXPENSE] += planned
        result[gmina_key][expense_data][rozdzial][EXECUTED_EXPENSE] += executed
        
        result[gmina_key]['__name'] = gmina_name

    return result

if os.path.exists(FILE_PICKLE):
    global DATA
    DATA = pickle.load(open(FILE_PICKLE, 'rb'))
else:
    DATA = generate_expenditures()
    pickle.dump(DATA, open(FILE_PICKLE, 'wb'))

def get_data_for_gmina(gmina, planned=False):
    gmina = gmina.lower()
    if not gmina in DATA:
        return
    gmina_info = DATA[gmina]
    result = {}
    for paragraph in gmina_info:
        if paragraph.startswith('__'):
            continue
        for chapter in gmina_info[paragraph]:
            if planned:
                result[chapter] = gmina_info[paragraph][chapter][EXECUTED_EXPENSE]
            else:
                result[chapter] = gmina_info[paragraph][chapter][PLANNED_EXPENSE]
    
    return result

def get_similar_gmina(gmina):
    return cities.cities.get_similar_city(gmina)

if __name__ == '__main__':
    from pprint import pprint
    pprint(get_data_for_gmina(u'Kraków'))
    print get_similar_gmina(u'Mysłowice')

