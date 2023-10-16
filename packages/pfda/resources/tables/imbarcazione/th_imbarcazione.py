#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tipo')
        r.fieldcell('nome',width='20em')
        r.fieldcell('flag')
        r.fieldcell('loa')
        r.fieldcell('gt')
        r.fieldcell('nt')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('tipo' )
        fb.field('nome' )
        #fb.field('bandiera' )
        fb.field('flag',columns='$nome,$code',auxColumns='$nome', limit=20 )
        fb.field('loa',validate_regex=" ^[0-9,]*$",validate_regex_error='Insert only numbers and comma', placeholder='eg: 10 or 10,50' )
        fb.field('gt',validate_regex=" ^[0-9,]*$",validate_regex_error='Insert only numbers and comma', placeholder='eg:1200 or 1200,00' )
        fb.field('nt' ,validate_regex=" ^[0-9,]*$",validate_regex_error='Insert only numbers and comma', placeholder='eg:650 or 650,00')
        fb.dataRpc('', self.ricercaImo, imo='^.imo', _onResult="""if(result!=null) {alert(result);}""")
        #fb.dataController("""if(msgspec==imo_nave) genro.publish("floating_message",{message:msg_txt, messageType:"message"});""",msgspec='^.imo',imo_nave='^imo_nave', msg_txt = 'Already existing name')


    @public_method
    def ricercaImo(self,imo):
        tbl_imbarcazioni = self.db.table('pfda.imbarcazione')
        imo_nave = tbl_imbarcazioni.readColumns(columns="""$imo AS imo_nave""", where='$imo=:imo', imo=imo)
        if imo_nave is not None:
            result = 'Already existing IMO. Please check before Save'
            return result

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
