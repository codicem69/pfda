#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('descrizione')
        r.fieldcell('file_url')

    def th_order(self):
        return 'descrizione'

    def th_query(self):
        return dict(column='descrizione', op='contains', val='')



class Form(BaseComponent):
    py_requires="""gnrcomponents/attachmanager/attachmanager:AttachManager"""

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.descrizioneTariffePortuali(bc.borderContainer(region='top',datapath='.record',height='80px'))
        tc = bc.tabContainer(region='center',margin='2px')
        self.allegatiTariffePortuali(tc.contentPane(title='Allegati'))
    
    def allegatiTariffePortuali(self,pane):
        pane.attachmentMultiButtonFrame()

    def descrizioneTariffePortuali(self,bc):
        left = bc.roundedGroup(region='center',title='Descrizione Tariffe Portuali').div(margin='10px',margin_right='20px')
        fb = left.formbuilder(cols=2, border_spacing='4px',colswidth='auto',fld_width='100%',width='100%')
        fb.field('descrizione',validate_notnull=True,validate_nodup=True)

    
    
    #def th_form(self, form):
     #   pane = form.record
      #  fb = pane.formbuilder(cols=2, border_spacing='4px')
       # fb.field('descrizione' )
        #fb.field('file_url' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
