#!/usr/bin/python
#coding:utf-8
###########################################################

###########################################################

import xapian
import sys
from collections import defaultdict
from mmseg.search import seg_txt_search, seg_txt_2_dict
import simplejson
import datetime
from decimal import Decimal

class Index(object):

    def __init__(self, DBPATH):
        self.SEARCH_DB = xapian.WritableDatabase(DBPATH, xapian.DB_CREATE_OR_OPEN)
    def _add_hanzi(self, doc, data):
        if not data:
            return 
        for word, value in seg_txt_2_dict(data).iteritems():
            doc.add_term(word, value)
    
    def _update_index(self, data_dict):
        doc = xapian.Document()
        self._add_hanzi(doc, data_dict['content'])
        key = 'I%s'%data_dict['id']
        doc.add_term(key)
        data = simplejson.dumps(data_dict, encoding='utf8')
        doc.set_data(data)
        self.SEARCH_DB.replace_document(key, doc)
        self.SEARCH_DB.flush()
 
class Search(object):
    def __init__(self, DBPATH):
        self.SEARCH_DB = xapian.Database(DBPATH)
        self.SEARCH_ENQUIRE = xapian.Enquire(self.SEARCH_DB)
    
    def _get_enquire_mset(self, start_offset, end_offset):
        try:
            return self.SEARCH_ENQUIRE.get_mset(start_offset, end_offset)
        except xapian.DatabaseModifiedError:
            self.SEARCH_DB.reopen()
            return self.SEARCH_ENQUIRE.get_mset(start_offset, end_offset)
            
    def _get_document_data(self, document):
        try:
            return document.get_data()
        except xapian.DatabaseModifiedError:
            self.SEARCH_DB.reopen()
            return document.get_data()
     
    def _get_hit_count(self):
        return self._get_enquire_mset(0, self.SEARCH_DB.get_doccount()).size()

    def search(self, keywords, start_offset=0, end_offset=None):
        query_list = []
        if isinstance(keywords, unicode):
            keywords = keywords.encode('utf8')
        for word, value in seg_txt_2_dict(keywords).iteritems():
            query = xapian.Query(word, value)
            query_list.append(query)
        if len(query_list) != 1:
            query = xapian.Query(xapian.Query.OP_OR, query_list)
        else:
            query = query_list[0]


        self.SEARCH_ENQUIRE.set_query(query)
        count = self.SEARCH_DB.get_doccount()
        if not end_offset:
            end_offset = count - start_offset

        matches = self._get_enquire_mset(start_offset, end_offset)
        
        results = []
        for match in matches:
            data = self._get_document_data(match.document)
            data = simplejson.loads(data, encoding='utf8')
            results.append(data)
        
        return {'count': self._get_hit_count(), 'object_list':results}

    def search_by_page(self, keywords, pagenum=1, num_per_page=20):
        if pagenum < 1:
            pagenum = 1
        start_offset = (pagenum - 1) * num_per_page
        end_offset = num_per_page
        data = self.search(keywords, start_offset, end_offset)
        data['has_previous'] = pagenum >1 and True or False
        data['previous_page_number'] = pagenum > 1 and pagenum - 1 or 1
        data['number'] = pagenum
        data['has_next'] = pagenum*num_per_page < data['count'] and True or False
        data['next_page_number'] = pagenum + 1
        data['paginator'] = {'num_pages': (data['count']+num_per_page-1) / num_per_page}
        return data


if __name__ == '__main__':
   pass 
