#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice')
        r.fieldcell('descrizione')
        r.fieldcell('valore')
        r.fieldcell('tariffa_tipo_id')

    def th_order(self):
        return 'codice'

    def th_query(self):
        return dict(column='descrizione', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('codice' ,validate_notnull=True)
        fb.field('descrizione',validate_notnull=True, width='30em' )
        fb.field('valore' ,validate_notnull=True)
        fb.field('tariffa_tipo_id' ,tag='hdbselect',validate_notnull=True,colspan=2, lbl='Tariffa Tipo')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
