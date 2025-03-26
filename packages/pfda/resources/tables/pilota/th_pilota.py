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
        r.fieldcell('ovt')
        r.fieldcell('pu')
        r.fieldcell('totpilot')

    def th_order(self):
        return 'proforma_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromPilot(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        #r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
        #                                    value='^.tariffa_id',
        #                                    rowcaption='$codice,$descrizione',
        #                                    auxColumns='@tariffa_tipo_id.descrizione',
        #                                    columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
        #                                    condition_cod='%pil%', 
        #                                    selected_valore='.pu',
        #                                    hasDownArrow=True))
        #
        #r.cell('quantita',name='Quantità',dtype='I',size='3',edit=True)
        #r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        #r.cell('pu',name='P.U.', dtype='N', size='10,2')
        #r.cell('tot',name='Totale Pilota', dtype='N', size='10,2',totalize='.sum_tot',formula='quantita*pu+quantita*pu*ovt/100',format='###,###,###.00')
        #r.fieldcell('totpilot', totalize=True, value='.tot')
        r.fieldcell('tariffe_id', edit=dict(validate_notnull=True,
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%pil%', hasDownArrow=True))#, edit=True, hasDownArrow=True,rowcaption='$codice,$descrizione')
        r.fieldcell('quantita',edit=True,default=1)#, edit=True)
        r.fieldcell('ovt',edit=True,default='0')#, edit=True)
        r.fieldcell('pu')
        r.fieldcell('totpilot', totalize='.totale_pilota', formula="pu*quantita+(ovt*quantita*pu/100)")
        #r.fieldcell('totpilot', totalize='.totale_pilota', formula='ovt>=0?pu*quantita+(ovt*quantita*pu/100):pu*quantita')

    #@public_method
    #def th_remoteRowController(self,row=None,field=None,**kwargs):
#
    #    field = field or 'tariffe_id' #nel caso di inserimento batch il prodotto viene considerato campo primario
    #    if not row['tariffe_id']:
    #        return row
    #    if not row['quantita']:
    #        row['quantita'] = 1
    #    if not row['ovt']:
    #        row['ovt'] = 0    
    #    if field == 'tariffe_id':
    #        prezzo_unitario = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=row['tariffe_id'])
    #        row['pu'] = prezzo_unitario  
    #    #qt=row['quantita']
    #    #pu=row['pu']
    #
    #    #totprest = decimalRound(qt * pu)
    #    totprest = decimalRound(row['quantita'] * row['pu'] )
    #    ovt = decimalRound(old_div(row['ovt'] * totprest,100))
    #    row['totpilot'] = decimalRound(totprest + ovt)
    #    return row

class ViewFromPilotCalc(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.cell('tariffa_id', edit=dict(remoteRowController=True,validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%pil%', hasDownArrow=True))#, edit=True, hasDownArrow=True,rowcaption='$codice,$descrizione')
        r.cell('qt',dtype='I',edit=dict(remoteRowController=True))#, edit=True)
        r.cell('ovtpil',dtype='N',size='3',edit=dict(remoteRowController=True))#, edit=True)
        r.cell('pupil', dtype='N', size='10,2')
        r.cell('totpilota', dtype='N', size='10,2', totalize=True)

    @public_method
    def th_remoteRowController(self,row=None,field=None,**kwargs):

        field = field or 'tariffa_id' #nel caso di inserimento batch il prodotto viene considerato campo primario
        if not row['tariffa_id']:
            return row
        if not row['qt']:
            row['qt'] = 1
        if not row['ovtpil']:
            row['ovtpil'] = 0    
        if field == 'tariffa_id':
            prezzo_unitario = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=row['tariffa_id'])
            row['pupil'] = prezzo_unitario  
        #qt=row['quantita']
        #pu=row['pu']
    
        #totprest = decimalRound(qt * pu)
        totprest = decimalRound(row['qt'] * row['pupil'] )
        ovt = decimalRound(old_div(row['ovtpil'] * totprest,100))
        row['totpilota'] = decimalRound(totprest + ovt)
        return row
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('proforma_id' )
        fb.field('tariffe_id' )
        fb.field('quantita' )
        fb.field('ovt' )
        fb.field('pu')
        fb.field('totpilot' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
