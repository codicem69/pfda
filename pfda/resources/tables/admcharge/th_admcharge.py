#!/usr/bin/python3
# -*- coding: utf-8 -*-

from past.utils import old_div
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import decimalRound

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('proforma_id')
        r.fieldcell('tariffe_id')
        r.fieldcell('quantita')
        r.fieldcell('pu')
        r.fieldcell('totadmcharge')

    def th_order(self):
        return 'proforma_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')


class ViewFromAdmcharge(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tariffe_id',edit=dict(remoteRowController=True,validate_notnull=True,
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',
                                            condition=":cod is NULL OR :cod = ''  OR $codice LIKE :cod",
                                            condition_cod='%Adm%', hasDownArrow=True))#, edit=True, hasDownArrow=True,rowcaption='$codice,$descrizione')
        r.fieldcell('quantita',edit=dict(remoteRowController=True))#, edit=True)
        r.fieldcell('pu')
        r.fieldcell('totadmcharge', totalize=True)
 
    @public_method
    def th_remoteRowController(self,row=None,field=None,**kwargs):

        field = field or 'tariffe_id' #nel caso di inserimento batch il prodotto viene considerato campo primario
        if not row['tariffe_id']:
            return row
        if not row['quantita']:
            row['quantita'] = 1
        
        if field == 'tariffe_id':
            prezzo_unitario = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=row['tariffe_id'])
            row['pu'] = prezzo_unitario  
                
        row['totadmcharge'] = decimalRound(row['quantita'] * row['pu'] )
        return row

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('proforma_id' )
        fb.field('tariffe_id' )
        fb.field('quantita' )
        fb.field('pu' )
        fb.field('totadmcharge' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
