#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime
from gnr.core.gnrlang import GnrException
from gnr.core.gnrnumber import floatToDecimal,decimalRound

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
        return 'protocollo:d'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')


    def th_query(self):
        return dict(column='id', op='contains', val='')

    
class ViewProforma(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('protocollo',width='11em')
        r.fieldcell('data',width='5em')
        r.fieldcell('cliente_id')
        r.fieldcell('imbarcazione_id', width='10em')
        r.fieldcell('cargo', width='10em')
        r.fieldcell('pilot')
        r.fieldcell('moor')
        r.fieldcell('tug')
        r.fieldcell('agency')
        r.fieldcell('customs',width='6em')
        r.fieldcell('garbage',width='5em')
        r.fieldcell('retaingarbage',width='5em')
        r.fieldcell('isps',width='5em')
        r.fieldcell('misc')
        r.fieldcell('bulkauth')
        r.fieldcell('antifire',width='5em')
        r.fieldcell('tot_servextra',width='5em')
        r.fieldcell('diritticp')
        r.fieldcell('admcharge',width='7em')
        r.fieldcell('stamp')
        r.fieldcell('totalepfda', background='lightyellow',font_weight='bold')
        r.fieldcell('timbro')
        r.fieldcell('pathtopdf', width='8em')
        #con la riga sottostante visualizziamo un bottone che ci fa aprire il pdf contenuto nel pathtopdf
        #r.fieldcell('pathtopdf', width='12em', template="""<button onclick="window.open('/_storage/home/proforma_ranalli/#');">proforma</button>""")
        #con la riga sottostante visualizziamo una lente d'ingradimento che ci fa aprire il pdf contenuto nel pathtopdf
        ag_id = self.db.currentEnv.get('current_agency_id')
        tbl_agency =  self.db.table('agz.agency')
        ag_code = tbl_agency.readColumns(columns='code',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        r.cell('apri tab', name="Proforma", width='5em', cellClasses='cellbutton',
               format_buttonclass='icnBaseLens buttonIcon',
               format_isbutton=True, format_onclick=f"""var row = this.widget.rowByIndex($1.rowIndex);
               genro.childBrowserTab('/_storage/home/proforma_{ag_code}/'+row['pathtopdf'].trim());""")
        
    def th_order(self):
        return 'data:d'

    def th_query(self):
        return dict(column='protocollo', op='contains', val='')

 

    def th_query(self):
        return dict(column='id', op='contains', val='')    

class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'
    #definiamo la form con la parte superiore e una parte inferiore
    def th_form(self, form):
        #bc = form.center.borderContainer()
        tc = form.center.tabContainer(selected='.current_tab')
        bc = tc.borderContainer(title='!![en]<strong>Proforma</strong>')
        #tc_edit = tc.tabContainer(title='!![en]<strong>Edit PFDA</strong>',region='center',selected='^.tabnumber')
        tc_print = tc.tabContainer(title='!![en]<strong>Print PFDA</strong>',region='center',selected='^.tabnumber')
        self.pfdaPDF(tc_print.framePane(title='!![EN]Print PFDA', datapath='#FORM.pdf'))
       
        #bcleft= form.center.borderContainer(margin='10px',text_align='center')
        #bcleft.contentPane(region='left',width='100px',
         #   background_color='lightyellow').div('Left')
     #   center = bc.tabContainer(region='center',margin='2px')
        #bc2=form.center.borderContainer()
        #tc = bc.borderContainer(region='right', width='50%').tabContainer(region='center',margin='2px')
        
        #qui sotto bcbmain se voglio inserire un'area nella parte in basso del proforma 
        #bcbmain = bc.borderContainer(region='bottom', height='10%',splitter=True)#.tabContainer(region='center',margin='2px')

        self.proformaTestata(bc.borderContainer(region='top',datapath='.record',height='150px'))
        self.proformaDett(bc.borderContainer(region='center',datapath='.record'))

        bc = bc.borderContainer(region='left', width='40%', splitter=True)#.borderContainer(region='top', height='50%')
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
        self.CostiAntifire(tc.borderContainer(title='Antifire/Antipollution'))
        #self.CostiAntifire(tc.contentPane(title='Antifire/Antipollution'))
        self.NoteProforma(tc.contentPane(title='Note Proforma',datapath='.record'))
        tc = bc.tabContainer(region='bottom',margin='2px',height='50%')
        self.calcoloPilota(tc.contentPane(title='Calcolo Pilota'))
        self.calcoloMoor(tc.contentPane(title='Calcolo Moor'))
        self.calcoloTug(tc.contentPane(title='Calcolo TUG'))
        
        #self.NoteProforma(bc.contentPane(title='Note Proforma',datapath='.record',region='bottom',margin='2px',height='50%'))
    #    self.proformaDettService(bc.borderContainer(region='bottom', datapath='.record', height='300px'))

    def proformaTestata(self,bc):
        bc.contentPane(region='center').linkerBox('cliente_id',margin='2px',openIfEmpty=True, validate_notnull=True,
                                                    columns='$nome,$indirizzo',
                                                    auxColumns='$email',
                                                    newRecordOnly=False,formResource='Form',
                                                    dialog_height='100px',dialog_width='600px')
        right = bc.roundedGroup(title='Dati proforma',region='right',width='60%')
        fb = right.formbuilder(cols=2, border_spacing='4px')
        #onDbChanges in caso di modifica dati su imbarcazione il form arrival viene aggiornato        
        fb.onDbChanges("""if(dbChanges.some(change=>change.dbevent=='U' && change.pkey==pkey)){this.form.reload()}""",
            table='pfda.imbarcazione',pkey='=#FORM.record.imbarcazione_id')
        
        fb.field('protocollo',width='22em',readOnly=True)
        fb.field('data',width='7em')
        fb.field('imbarcazione_id',width='22em')
        #fb.field('bandiera',width='28em')
        fb.field('@imbarcazione_id.@flag.codename',width='28em',lbl='!![en]Flag', readOnly=True)
        fb.field('@imbarcazione_id.gt',width='7em', readOnly=True)
        fb.field('@imbarcazione_id.nt',width='7em', readOnly=True)
        fb.field('@imbarcazione_id.loa',width='7em', readOnly=True)
        fb.field('cargo',width='28em' )
        fb.field('dangerous_cargo', default=False, hidden='^#FORM.record.imbarcazione_id?=#v==null')
        fb.checkbox(value='^.tributi', lbl='Disattiva tributi')
        fb.dataRpc('.diritticp', self.calcoloTributi, dangerouscargo='^.dangerous_cargo',imb='^.imbarcazione_id',gt='=#FORM.record.@imbarcazione_id.gt',_if='imb',
                       _onResult='this.form.save();', calc_trib='^.tributi')
        
    
    @public_method
    def calcoloTributi(self, dangerouscargo=None, gt=None,calc_trib=None,**kwargs):
        tbl_tributi=self.db.table('pfda.tributicp')
        tributi = tbl_tributi.query(columns="$importo,$descrizione",
                         where='').fetch()
        for r in tributi:
            if int(gt) < 250:
                if r['descrizione'] == '<250':
                    importo=r['importo']
            if int(gt) >= 250:
                if r['descrizione'] == '=>250':
                    importo=r['importo']    
        if dangerouscargo == True:
            importo = importo * 2
        importo = floatToDecimal(importo) + floatToDecimal(0.50)
        if calc_trib == True:
            importo = None
            
        return importo

    
    
    def proformaDett(self,bc):
        #fb = pane.div(margin_left='10px',margin_right='180px').formbuilder(title='Costi Servizi',cols=2, border_spacing='4px',colswidth='30px',fld_width='100%')
               
        rightdett = bc.roundedGroup(title='Costi servizi',region='right', width='100%')
       
        fb = rightdett.formbuilder(cols=2, border_spacing='4px',margin='4px')
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
        fb.field('garbage',width='5em')#, default_value=450)
        fb.field('notegarbage',width='20em' )
        fb.field('retaingarbage',width='5em' )
        fb.field('noteretaingb',lbl='note Garb.auth',width='20em' )
        fb.field('isps',width='5em' )
        fb.field('noteisps',width='20em' )
        fb.field('misc',width='5em' )
        fb.field('notemisc',width='20em' )
        fb.field('bulkauth',width='5em' )
        fb.field('notebulk',width='20em' )
        fb.field('antifire',width='5em' )
        fb.field('noteantifire',width='20em' )
        fb.field('tot_servextra',width='5em' )
        fb.br()
        #fb.dbSelect(dbtable='pfda.tributicp',lbl='Scelta TributiCP',auxColumns='$descrizione,$importo',
        #            selected_importo='.diritticp',
        #                hasDownArrow=True)
        fb.field('diritticp',width='5em',
                    tooltip="""Sotto GT 250 € 31,00 - da GT 250 in su € 62,00 - Petroliere o Merce pericolosa il Doppio della Tariffa""" )
        fb.br()
        fb.field('admcharge',lbl='adm charge',width='5em' )
        fb.br()
        fb.field('stamp',width='5em' )
        fb.field('totalepfda',width='10em',lbl_font_weight='bold',font_weight='bold' )
        fb.numberTextBox('^.totalepfda',lbl='Totale pfda',readOnly=True,width='10em')
        fb.checkbox(value='^.timbro', lbl='Timbro Società: ', label='Confermato')



        

        fb.dataFormula('^.totalepfda','a+b+c+d+e+f+g+h+i+l+m+n+o+p+q', a='^.pilot', b='^.moor', c='^.tug', d='^.agency', e='^.customs',
                                        f='^.garbage', g='^.retaingarbage', h='^.isps', i='^.misc', l='^.bulkauth', 
                                        m='^.diritticp', n='^.antifire', o='^.tot_servextra', p='^.admcharge', q='^.stamp' )

           
        # creiamo un bottone che inserisce i valori fissi prelevandoli dai valori inseriti nelle preference di sistema
        fb.br()
        fb.button('Inserisci',lbl='Tariffe Standard',action="""SET .garbage = garb;
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
        fb.br()
        fb.div(' ')
        
        #email_account_id = self.db.application.getPreference('mail.account_id',pkg='pfda')
        #email_template_id = self.db.application.getPreference('tpl.template_id',pkg='pfda')

        #btn = fb.Button('Crea Email',lbl='Email Proforma')
        #btn.dataRpc('msg_special', self.invia_proforma,_ask="Hai creato il PDF con la stampa proforma? <br/> Altrimenti non ci sarà l'allegato nell'email",#self.db.table('pfda.proforma').invia_proforma,
        #           record='=#FORM.record',
        #           email_account_id=email_account_id,
        #           email_template_id=email_template_id)
        #fb.dataController("""if(msgspec=='proforma') genro.publish("floating_message",{message:msg_txt, messageType:"message"});""",msgspec='^msg_special', msg_txt = 'Email ready to be sent')
        # qua verifichiamo di aver settato nelle preferenze del proforma l'account email e il template da utilizzare
        # nel caso  saremo avvisati da un msg alert
        #if (email_account_id and email_template_id) == None:
             #raise GnrException('purtroppo manca questa cosa ')
            #fb.data('.messaggio_speciale', "Verifica di aver inserito nelle preferenze globali \n l'account email e il template da utilizzare per l'invio dell'email")
            #fb.dataController('alert(msg)', msg='=.messaggio_speciale', _if='msg', _onStart=True)
           
           # se al posto dell'alert volevamo inserire un div
           #fb.div(' ')
           #fb.div("Verifica di aver inserito nelle preferenze globali <br/> l'account email e il template da utilizzare per l'invio dell'email",
           #      color='white',
           #      background='red',
           #      font_size='12px',
           #      font_weight='bold',
           #      margin='5px', border='2px solid yellow',
           #      text_align='center',
           #      padding='4px',
           #      shadow='3px 3px 6px silver')
       
    def pfdaPDF(self,frame):
        self.printDisplay(frame,resource='pfda.proforma:html_res/stampaprof')
    
    def printDisplay(self, frame, resource=None, html=None):
        bar = frame.top.slotBar('10,lett_select,*', height='20px', border_bottom='1px solid silver')
        bar.lett_select.formbuilder().dbselect('^.curr_letterhead_id',
                                                table='adm.htmltemplate',
                                                lbl='Carta intestata',
                                                hasDownArrow=True)
        frame.documentFrame(resource=resource,
                            pkey='^#FORM.pkey',
                            html=html,
                            letterhead_id='^.curr_letterhead_id',
                            missingContent='NO Proforma',
                            _if='pkey',_delay=100)
        
        
    def CostiOrm(self,pane):
        #rightbc = bc.roundedGroup(title='Costi Ormegg')
        #fb = rightbc.formbuilder(cols=2, border_spacing='4px')
        #fb.field('pilot',width='5em' )
        pane.inlineTableHandler(relation='@proforma_orm',viewResource='ViewFromOrmeggiatori')

    def CostiPilota(self,pane):
        #rightbc = bc.roundedGroup(title='Cosmail.account_idti Pilota')
        #fb = rightbc.formbuilder(cols=2, border_spacing='4px')
        #fb.field('pilot',width='5em' )
        pane.inlineTableHandler(relation='@proforma_pilota',viewResource='ViewFromPilot')

    def calcoloPilota(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_pilota.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'calcolo pilota'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_pilot,datapath='.calcolo_pilota',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True) 

    def calcoloMoor(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_moor.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'calcolo moor'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_moor,datapath='.calcolo_moor',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)

    def calcoloTug(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_tug.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'calcolo tug'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_tug,datapath='.calcolo_tug',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)
        
    def struct_pilot(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%pil%', 
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('qt',name='Quantità',dtype='I',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale Pilota', dtype='N', size='10,2',totalize='.sum_tot',formula='qt*valore+qt*valore*ovt/100',format='###,###,###.00')

    def struct_moor(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%orm%', 
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('qt',name='Quantità',dtype='N',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale Moor',dtype='N',formula='qt*valore+qt*valore*ovt/100',totalize='.sum_moor',format='###,###,###.00')  

    def struct_tug(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%tug%',
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('n_tug',name='Numero Tug',dtype='N',size='3',edit=True)
        r.cell('qt',name='Quantità prestazioni',dtype='N',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale TUG',dtype='N',formula='n_tug*valore*qt+n_tug*valore*qt*ovt/100',totalize='.sum_tug',format='###,###,###.00')

    def CostiTug(self,pane):
        pane.inlineTableHandler(relation='@proforma_tug',viewResource='ViewFromTug')  

    def CostiAgency(self,pane):
        pane.inlineTableHandler(relation='@proforma_agency',viewResource='ViewFromAgency')  

    def CostiCustoms(self,pane):
        pane.inlineTableHandler(relation='@proforma_customs',viewResource='ViewFromCustoms')      
    
    def CostiAdmcharge(self,pane):
        pane.inlineTableHandler(relation='@proforma_admcharge',viewResource='ViewFromAdmcharge')

    def CostiServiziExtra(self,pane):
        pane.inlineTableHandler(relation='@proforma_servextra',viewResource='ViewFromServiziExtra',
                                picker='servizi_id',picker_viewResource='View')

    def CostiAntifire(self,bc):
        cp = bc.contentPane(region='center')
        cp2 = bc.contentPane(region='top', height='10%').div('Tariffe Orario Normale Feriale Lunedì/Venerdì 0800/1200 1400/1800 ')
        cp.inlineTableHandler(relation='@proforma_antifire',viewResource='ViewFromAntifire')

    def NoteProforma(self,frame):
        frame.simpleTextArea(title='Extra',value='^.noteproforma',editor=True)
    #def NoteProforma(self,bc):
        #bc.roundedGroup(title='Extra',value='^.noteproforma',editor=True)

    #def th_hiddencolumns(self):
     #       return "$garbageval"

    def th_bottom_custom(self, bottom):
        bar = bottom.slotBar('*,stampa_proforma,5,crea_email,*,10')
        bar.stampa_proforma.button('Stampa Proforma', iconClass='print',
                                    action="""genro.publish("table_script_run",{table:"pfda.proforma",
                                                                               res_type:'print',
                                                                               resource:'stampa_proforma',
                                                                               pkey: pkey})""",
                                                                               pkey='=#FORM.pkey')

        email_account_id = self.db.application.getPreference('mail.account_id',pkg='pfda')
        email_template_id = self.db.application.getPreference('tpl.template_id',pkg='pfda')
        btn_creaemail=bar.crea_email.button('Crea email proforma')
        btn_creaemail.dataRpc('msg_special', self.invia_proforma,_ask="Hai creato il PDF con la stampa proforma? <br/> Altrimenti non ci sarà l'allegato nell'email",#self.db.table('pfda.proforma').invia_proforma,
                   record='=#FORM.record',
                   email_account_id=email_account_id,
                   email_template_id=email_template_id)
        bar.dataController("""if(msgspec=='proforma') genro.publish("floating_message",{message:msg_txt, messageType:"message"});""",msgspec='^msg_special', msg_txt = 'Email ready to be sent')
        # qua verifichiamo di aver settato nelle preferenze del proforma l'account email e il template da utilizzare
        # nel caso  saremo avvisati da un msg alert
        if (email_account_id and email_template_id) == None:
            #raise GnrException('purtroppo manca questa cosa ')
            bar.data('.messaggio_speciale', "Verifica di aver inserito nelle preferenze globali \n l'account email e il template da utilizzare per l'invio dell'email")
            bar.dataController('alert(msg)', msg='=.messaggio_speciale', _if='msg', _onStart=True)
        
    def th_options(self):
        return dict(dialog_windowRatio = 1, annotations= True, duplicate=True )
        #return dict(dialog_height='400px', dialog_width='600px', dialog_parentRatio=1 )


    
    @public_method
    def invia_proforma(self, record,email_account_id,email_template_id, **kwargs):
        tbl_proforma = self.db.table('pfda.proforma')
        if not record: 
            return
        
        record_id=record['id']
        nome_file=record['pathtopdf']
        pdfpath = self.site.storageNode('home:proforma', nome_file)
        attcmt = [pdfpath.internal_path]

        #verifichiamo il secondo allegato info port nella tabella fileforemail
        tbl_file =  self.db.table('pfda.fileforemail') #definiamo la variabile della tabella allegati
        att = tbl_file.query(columns="$pathfile", where='').fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            #url_att = url_allegato.replace('home:','site/')#cambiamo al url_allegato la posizione home: in site/
            #print(x)
            attcmt.append(url_allegato)#appendiamo agli attcmt l'url_allegato aggiungendoci il path iniziale

        self.db.table('email.message').newMessageFromUserTemplate(
                                                      record_id=record_id,
                                                      table='pfda.proforma',
                                                      attachments=attcmt,
                                                      account_id = email_account_id,
                                                      template_id=email_template_id)
        
        self.db.commit()
        msg_special='proforma'
        return msg_special

    def invia_proforma2(self, record, resultAttr=None, **kwargs):
       
        # Crea stampa   
        #print(ciao)
        tbl_proforma = self.db.table('pfda.proforma')
        if not record: 
            return
        builder = TableTemplateToHtml(table=tbl_proforma)   
        
        nome_template = 'pfda.template:test'
        #nome_template = 'pfda.proforma:test'
        
        prot_proforma = self.db.table('pfda.proforma').readColumns(columns='$protocollo', where='$id=:f_id', f_id=record)
        prot_proforma = prot_proforma.replace("/", "_")
        nome_file = '{cl_id}.pdf'.format(
                    cl_id=prot_proforma[:-1])#record[0:])
        template = self.loadTemplate(nome_template)  # nome del template
        print(ciao)
        pdfpath = self.site.storageNode('home:proforma_ranalli', nome_file)
        #pdfpath_st = self.site.storageNode('home:proforma', nome_file_st) # (pdfpath.internal_path)
        builder(record=record, template=template)
        result = builder.writePdf(pdfpath=pdfpath)
        #result = builder.writePdf(pdfpath=pdfpath_st)
        #print(ciao)
        self.setInClientData(path='gnr.clientprint',
                             value=result.url(timestamp=datetime.now()), fired=True)
    
    
