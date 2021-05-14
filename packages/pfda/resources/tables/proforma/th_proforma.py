#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrnumber import decimalRound
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('data')
        r.fieldcell('cliente_id')
        r.fieldcell('imbarcazione_id')
        r.fieldcell('cargo')
        r.fieldcell('pilot')
        r.fieldcell('notepilot')
        r.fieldcell('moor')
        r.fieldcell('notemoor')
        r.fieldcell('tug')
        r.fieldcell('notetug')
        r.fieldcell('agency')
        r.fieldcell('noteagency')
        r.fieldcell('customs')
        r.fieldcell('notecustoms')
        r.fieldcell('garbage')
        r.fieldcell('notegarbage')
        r.fieldcell('retaingarbage')
        r.fieldcell('noteretaingb')
        r.fieldcell('isps')
        r.fieldcell('noteisps')
        r.fieldcell('misc')
        r.fieldcell('notemisc')
        r.fieldcell('bulkauth')
        r.fieldcell('notebulk')
        r.fieldcell('diritticp')
        r.fieldcell('admcharge')
        r.fieldcell('stamp')
        r.fieldcell('totalepfda')

    def th_order(self):
        return 'protocollo'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')

    def th_order(self):
        return 'proforma_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

    
class ViewProforma(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo')
        r.fieldcell('data')
        r.fieldcell('cliente_id')
        r.fieldcell('imbarcazione_id')
        r.fieldcell('cargo')
        r.fieldcell('pilot')
        r.fieldcell('moor')
        r.fieldcell('tug')
        r.fieldcell('agency')
        r.fieldcell('customs')
        r.fieldcell('garbage')
        r.fieldcell('retaingarbage')
        r.fieldcell('isps')
        r.fieldcell('misc')
        r.fieldcell('bulkauth')
        r.fieldcell('diritticp')
        r.fieldcell('admcharge')
        r.fieldcell('stamp')
        r.fieldcell('totalepfda')

    def th_order(self):
        return 'protocollo'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')

    def th_order(self):
        return 'proforma_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

    

class Form(BaseComponent):
    #definiamo la form con la parte superiore e una parte inferiore
    def th_form(self, form):
        bc = form.center.borderContainer()
        #bcleft= form.center.borderContainer(margin='10px',text_align='center')
        #bcleft.contentPane(region='left',width='100px',
         #   background_color='lightyellow').div('Left')
     #   center = bc.tabContainer(region='center',margin='2px')
        #bc2=form.center.borderContainer()
        #tc = bc.borderContainer(region='right', width='50%').tabContainer(region='center',margin='2px')
        
        #qui sotto bcbmain se voglio inserire un'area nella parte in basso del proforma 
        #bcbmain = bc.borderContainer(region='bottom', height='10%',splitter=True)#.tabContainer(region='center',margin='2px')

        self.proformaTestata(bc.borderContainer(region='top',datapath='.record',height='120px'))
        self.proformaDett(bc.borderContainer(region='center',datapath='.record'))

        bc = bc.borderContainer(region='right', width='50%', splitter=True)#.borderContainer(region='top', height='50%')
        tc = bc.tabContainer(region='center',margin='2px')
        
        #bc = bc(region='center',margin='2px')
        #bc = bc.borderContainer(region='bottom', height='10%',splitter=True).tabContainer(region='center',margin='2px')
        
        #self.CostiOrm(tc.borderContainer(title='Ormeggiatori'))
        self.CostiPilota(tc.contentPane(title='Pilota'))
        self.CostiOrm(tc.contentPane(title='Ormeggiatori'))
        self.CostiTug(tc.contentPane(title='Tug'))
        self.CostiAgency(tc.contentPane(title='Agency'))
        self.CostiCustoms(tc.contentPane(title='Customs'))
        self.CostiAdmcharge(tc.contentPane(title='Adm Charge'))
        self.CostiServiziExtra(tc.contentPane(title='Servizi Extra'))
        
        #self.CostiAntifire(tc.contentPane(title='Antifire/Antipollution'))
        self.NoteProforma(tc.contentPane(title='Note Proforma',datapath='.record'))
        tc = bc.tabContainer(region='bottom',margin='2px',height='50%')
        self.CostiAntifire(tc.borderContainer(title='Antifire/Antipollution'))
        
        #self.NoteProforma(bc.contentPane(title='Note Proforma',datapath='.record',region='bottom',margin='2px',height='50%'))
    #    self.proformaDettService(bc.borderContainer(region='bottom', datapath='.record', height='300px'))

    def proformaTestata(self,bc):
        bc.contentPane(region='center').linkerBox('cliente_id',margin='2px',openIfEmpty=True, validate_notnull=True,
                                                    columns='$nome,$indirizzo',
                                                    auxColumns='$email',
                                                    newRecordOnly=True,formResource='Form',
                                                    dialog_height='100px',dialog_width='600px')
        left = bc.roundedGroup(title='Dati proforma',region='left',width='65%')
        fb = left.formbuilder(cols=2, border_spacing='4px')
        fb.field('protocollo',width='8em',readOnly=True)
        fb.field('data',width='7em')
        fb.field('imbarcazione_id',width='22em')
        fb.field('bandiera',width='28em')
        fb.field('gt',width='7em')
        fb.field('nt',width='7em')
        fb.field('loa',width='7em')
        fb.field('cargo',width='28em' )
    
    
    def proformaDett(self,bc):
        #fb = pane.div(margin_left='10px',margin_right='180px').formbuilder(title='Costi Servizi',cols=2, border_spacing='4px',colswidth='30px',fld_width='100%')
               
        leftdett = bc.roundedGroup(title='Costi servizi',region='left', width='100%')
       
        fb = leftdett.formbuilder(cols=2, border_spacing='4px',margin='4px')
        fb.field('pilot',width='5em')
        fb.field('notepilot',width='20em' )
        fb.field('moor',width='5em')
        fb.field('notemoor',width='20em' )
        fb.field('tug',width='5em' )
        fb.field('notetug',width='20em' )
        fb.field('agency',width='5em' )
        fb.field('noteagency',width='20em' )
        fb.field('customs',width='5em' )
        fb.field('notecustoms',width='20em' )
        fb.field('garbage',width='5em', default_value=190)
        fb.field('notegarbage',width='20em' )
        fb.field('retaingarbage',width='5em' )
        fb.field('noteretaingb',lbl='note Garb.auth',width='20em' )
        fb.field('isps',width='5em' )
        fb.field('noteisps',width='20em' )
        fb.field('misc',width='5em' )
        fb.field('notemisc',width='20em' )
        fb.field('bulkauth',width='5em' )
        fb.field('notebulk',width='20em' )
        fb.field('diritticp',width='5em',
                    tooltip="""Sotto GT 250 € 31,00 - da GT 250 in su € 62,00 - Petroliere o Merce pericolosa il Doppio della Tariffa""" )
        fb.br()
        fb.field('admcharge',lbl='adm charge',width='5em' )
        fb.br()
        fb.field('stamp',width='5em' )
        fb.field('totalepfda',width='10em',lbl_font_weight='bold',font_weight='bold' )
        #fb.numberTextBox('^.totalepfda',lbl='Totale pfda',readOnly=True,width='10em')

        fb.dataFormula('^.totalepfda','a+b+c+d+e+f+g+h+i+l+m+n+o', a='^.pilot', b='^.moor', c='^.tug', d='^.agency', e='^.customs', 
                                        f='^.garbage', g='^.retaingarbage', h='^.isps', i='^.misc', l='^.bulkauth', 
                                        m='^.diritticp', n='^.admcharge', o='^.stamp' )

           
        # creiamo un bottone che inserisce i valori fissi prelevandoli dai valori inseriti nelle preference di sistema
        fb.button('Inserisci',lbl='Inserisci Tariffe Standard',action="""SET .garbage = garb;
                                                                         SET .retaingarbage = retaingarb;
                                                                         SET .isps = security;
                                                                         SET .misc = varie;
                                                                         SET .notemisc = ntmisc;
                                                                        SET .bulkauth = bulkaut;
                                                                        alert("Inserito - Ricordati di salvare");""",
                    garb='=gnr.app_preference.pfda.garbage_df', 
                    retaingarb='=gnr.app_preference.pfda.retaingarbage_df',
                    security='=gnr.app_preference.pfda.isps_df',
                    varie='=gnr.app_preference.pfda.misc_df',
                    ntmisc='=gnr.app_preference.pfda.notemisc_df',
                    bulkaut='=gnr.app_preference.pfda.bulkauth_df')
    
    # ---------------------    
    # prelevare dati avendo un record specifico e inserirli nei campi tramite bottone            
    #    fb.Button('Inserisci',lbl='Inserisci Tariffe Standard',fire='preleva')
        
    #    fb.dataRpc('risultato_rpc', self.preleva,_fired='^preleva')
    
    #    fb.dataController("""
    #        var garbval=genro.getData('risultato_rpc.record.garbageval')
    #        genro.setData('pfda_proforma.form.record.garbage',garbval)
    #        var garbret=genro.getData('risultato_rpc.record.retaingarbage')
    #        genro.setData('pfda_proforma.form.record.retaingarbage',garbret)
    #        var ispsv=genro.getData('risultato_rpc.record.ispsval')
    #        genro.setData('pfda_proforma.form.record.isps',ispsv)
    #        var miscv=genro.getData('risultato_rpc.record.miscval')
    #        genro.setData('pfda_proforma.form.record.misc',miscv)
    #        var bulkv=genro.getData('risultato_rpc.record.bulkval')
    #        genro.setData('pfda_proforma.form.record.bulkauth',bulkv)
    #        var notemiscv=genro.getData('risultato_rpc.record.notemiscval')
    #        genro.setData('pfda_proforma.form.record.notemisc',notemiscv);
    #        alert("Inserito - Ricordati di salvare");""",fired='^risultato_rpc')

    
    
    #@public_method
    #def preleva(self):
    #    result = Bag()
    #    tbl_valorifissi = self.db.table('pfda.valorifissi')
    #    dati_fissi = tbl_valorifissi.record('xAU5beK_P0SJqcqpdOeq6A').output('dict')
    #    if dati_fissi:
    #        result['record'] = Bag(dict(garbageval=dati_fissi['garbageval'],
    #                                    retaingarbage=dati_fissi['retaingarbval'],
    #                                    ispsval=dati_fissi['ispsval'],
    #                                    miscval=dati_fissi['miscval'],
    #                                    bulkval=dati_fissi['bulkval'],
    #                                    notemiscval=dati_fissi['notemiscval']))
    #        result['ok'] = 'Trovato'
    #    else:
    #        result['nuovo'] = 'Nuovo'
    #    return result    

    #---------------------------------
    #@public_method
    #def preleva(self, f=None):
    #        f=self.db.table('pfda.valorifissi').query(columns='$garbageval').fetch()
    #        return f[0]

    # -------------------------------
    #    fb.dataRpc('dummy', self.cercaValorifissi,
    #                garbageval='^.garbageval',
    #                _if='garbageval&&this.form.isNewRecord()',
    #                _userChanges=True,
    #                _onResult="""if(result.getItem('ok')){
    #                                var record = GET #FORM.record;
    #                                record.update(result.getItem('record'));
    #                            };
    #                """)      
    
    #@public_method
    #def cercaValorifissi(self, garbageval=None):
    #    result = Bag()
    #    tbl_valorifissi = self.db.table('pfda.valorifissi')
    #    dati_fissi = tbl_valorifissi.record(
    #        garbageval=garbageval, ignoreMissing=True).output('dict')
    #    if dati_fissi:
    #        result['record'] = Bag(dict(retaingarbage=dati_fissi['retaingarbval'],
    #                                    isps=dati_fissi['ispsval'],
    #                                    misc=dati_fissi['miscval'],
    #                                    bulkauth=dati_fissi['bulkval'],
    #                                    notemisc=dati_fissi['notemiscval']))
    #        result['ok'] = 'Trovato'
    #    else:
    #        result['nuovo'] = 'Nuovo'
    #    return result    
    #-----------------------------

    def CostiOrm(self,pane):
        #rightbc = bc.roundedGroup(title='Costi Ormegg')
        #fb = rightbc.formbuilder(cols=2, border_spacing='4px')
        #fb.field('pilot',width='5em' )
        pane.inlineTableHandler(relation='@proforma_orm',viewResource='ViewFromOrmeggiatori')

    def CostiPilota(self,pane):
        #rightbc = bc.roundedGroup(title='Costi Pilota')
        #fb = rightbc.formbuilder(cols=2, border_spacing='4px')
        #fb.field('pilot',width='5em' )
        pane.inlineTableHandler(relation='@proforma_pilota',viewResource='ViewFromPilot')                           

    def CostiTug(self,pane):
        pane.inlineTableHandler(relation='@proforma_tug',viewResource='ViewFromTug')  

    def CostiAgency(self,pane):
        pane.inlineTableHandler(relation='@proforma_agency',viewResource='ViewFromAgency')  

    def CostiCustoms(self,pane):
        pane.inlineTableHandler(relation='@proforma_customs',viewResource='ViewFromCustoms')      
    
    def CostiAdmcharge(self,pane):
        pane.inlineTableHandler(relation='@proforma_admcharge',viewResource='ViewFromAdmcharge')

    def CostiServiziExtra(self,pane):
        pane.inlineTableHandler(relation='@proforma_servextra',viewResource='ViewFromServiziExtra')    

    def CostiAntifire(self,bc):
        cp = bc.contentPane(region='center')
        cp2 = bc.contentPane(region='top', height='10%').div('Tariffe Orario Normale Feriale Lunedì/Venerdì 0800/1200 1400/1800 ')
        cp.inlineTableHandler(relation='@proforma_antifire',viewResource='ViewFromAntifire')

    def NoteProforma(self,frame):
        frame.simpleTextArea(title='Extra',value='^.noteproforma',editor=True)
    #def NoteProforma(self,bc):
        #bc.roundedGroup(title='Extra',value='^.noteproforma',editor=True)

    def th_hiddencolumns(self):
            return "$garbageval"

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
