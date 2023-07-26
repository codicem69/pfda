#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('id')
        #r.fieldcell('garbageval')
        r.fieldcell('garbageval')
        r.fieldcell('retaingarbval')
        r.fieldcell('ispsval')
        r.fieldcell('miscval')
        r.fieldcell('bulkval')
        r.fieldcell('notemiscval')

    def th_order(self):
        return 'id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        #fb.field('id')#, readOnly=True )
        fb.field('garbageval' )
        fb.field('retaingarbval' )
        fb.field('ispsval' )
        fb.field('miscval' )
        fb.field('bulkval' )
        fb.field('notemiscval' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
