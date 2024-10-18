#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('nome',width='20em')
        r.fieldcell('indirizzo',width='30em')
        r.fieldcell('tel',width='20em')
        r.fieldcell('email',width='20em')
        r.fieldcell('email_cc',width='20em')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('nome')
        fb.field('indirizzo' )
        fb.field('tel' )
        fb.field('email' )
        fb.field('email_cc' )
        

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

class FormCliente(BaseComponent):

   #def th_form(self, form):
   #    pane = form.record
   #    fb = pane.formbuilder(cols=1, border_spacing='4px')
   #    fb.field('nome', width='40em' )
   #    fb.field('indirizzo', width='100em' )
   #    fb.field('tel', width='40em' )
   #    fb.div('Inserire le email separate dalla virgola')
   #    fb.field('email', width='100em' )
   #    fb.field('email_cc', width='100em' )
        
    def th_form(self,form):
        bc = form.center.borderContainer()
        self.datiCliente(bc.roundedGroupFrame(title='Dati cliente',region='top',datapath='.record',height='185px', splitter=True))
        tc = bc.tabContainer(region = 'center',margin='2px')
        self.proformaCliente(tc.contentPane(title='Proforma'))
        self.noteCliente(tc.contentPane(title='Note',datapath='.record'))

    def datiCliente(self,pane):
        fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=1, border_spacing='4px',colswidth='auto',fld_width='100%')
        fb.field('nome', colspan=2,validate_onAccept='FIRE #FORM.nome')
        fb.field('indirizzo',colspan=2)
        fb.field('tel')
        fb.div('Inserire le email separate dalla virgola')
        fb.field('email')
        fb.field('email_cc' )
        fb2 = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=3)    
        fb.dataRpc('', self.ricercaCliente, cliente='=.nome',_fired='^#FORM.nome', _onResult="""if(result!=null) {alert(result);}""")
        


    @public_method
    def ricercaCliente(self,cliente):
        tbl_imbarcazioni = self.db.table('pfda.cliente')
        cliente_pfda = tbl_imbarcazioni.readColumns(columns="""$nome AS nome_cliente""", where='$nome=:cliente', cliente=cliente)
        if cliente_pfda is not None:
            result = 'Already existing Customer. Please check before Save'
            return result
        
    def proformaCliente(self,pane):
        pane.dialogTableHandler(relation='@cliente',
                                viewResource='ViewProforma')

    def noteCliente(self,frame):
        frame.simpleTextArea(value='^.note',editor=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
