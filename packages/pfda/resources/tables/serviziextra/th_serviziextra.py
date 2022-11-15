#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('proforma_id')
        r.fieldcell('servizi_id')
        r.fieldcell('descrizione')
        r.fieldcell('tariffa')

    def th_order(self):
        return '_row_count'

    def th_query(self):
        return dict(column='servizi_id', op='contains', val='')

class ViewFromServiziExtra(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('servizi_id', hasDownArrow=True, edit=True)
        r.fieldcell('descrizione',width='36em', edit=True)
        r.fieldcell('tariffa', edit=True, totalize=True)
    
    def th_order(self):
        return '_row_count'
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('proforma_id' )
        fb.field('servizi_id' )
        fb.field('descrizione' )
        fb.field('tariffa' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
