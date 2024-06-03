 
from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from gnr.core.gnrstring import slugify
from gnr.core.gnrdecorator import public_method
from gnr.app.gnrapp import GnrApp

caption = 'Email Proforma'

class Main(BaseResourcePrint):
    batch_title = 'Email_Prof'
    batch_immediate='download'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/stampaprof'
    #templates = 'Ranalli_st'
    mail_address='@cliente_id.email'
    batch_print_modes = ['pdf','mail_deliver']
    #Non utilizziamo il table_script_parameters_pane perché ci limiteremo a stampare la selezione corrente
    
   # def table_script_parameters_pane(self, pane,**kwargs):
   #     ag_id = self.db.currentEnv.get('current_agency_id')
   #     print(ag_id)
     #   fb = pane.formbuilder(cols=1, width='220px')
     #   fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
    def pre_process(self):
        ag_id = self.db.currentEnv.get('current_agency_id')

        tbl_agency =  self.db.table('agz.agency')
        htmltemplate_id = tbl_agency.readColumns(columns='htmltemplate_id',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        carta_intestata = tbl_htmltemplate.readColumns(columns='name',
                            where='$id=:htmltemplate_id', htmltemplate_id=htmltemplate_id)
        #templates = 'Ranalli_st'
        self.templates = carta_intestata
        self.htmlMaker = self.page.site.loadTableScript(page=self.page, table='pfda.proforma',
                                                        respath='html_res/stampaprof', class_name='Main')
    def onRecordPrinted(self, record, filepath=None):
        tbl_proforma = self.db.table('pfda.proforma')
        if not record: 
            return
        
        builder = TableTemplateToHtml(table=tbl_proforma)
        builder(record=record)
        prot_proforma = record['protocollo']
        prot_proforma = prot_proforma.replace("/", "")
        nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_proforma[:-1]))#record[0:])
        pdfpath = self.page.site.storageNode('home:proforma', nome_file)
        #pdfpath = self.page.site.storageNode('/home/tommaso/Documenti/Agenzia/PROFORMA', nome_file)
        #result = builder.writePdf(pdfpath=pdfpath)
        #self.setInClientData(path='gnr.clientprint',
        #                     value=result.url(timestamp=datetime.now()), fired=True)
        page = self.page
        #slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')
        #self.outputFileNode(page)
        id_record = record['id']
        percorso_pdf = pdfpath.internal_path

        #result = builder.writePdf(pdfpath=pdfpath)
       #if percorso_pdf is not None:
       #
       #    record['pathtopdf'] = percorso_pdf
       #
       #    self.db.commit()
        #record['pathtopdf']=percorso_pdf

       #app = GnrApp('pfda')
       #mydb = app.db
       #tbl_proforma = mydb.table('pfda.proforma')
       #rec_proforma = tbl_proforma.record(where='$id=:id_prof', 
       #                          id_prof=id_record,
       #                          for_update=True).output('dict')
       #old_record = dict(rec_proforma)
       #rec_proforma['pathtopdf'] = percorso_pdf
       #tbl_proforma.update(rec_proforma, old_record)
       #
       #mydb.commit()

        #print(c)
        #inserisciPathPdf

   #def inserisciPathPdf(self,record):
   #    proforma_id = record['id_record']
   #    self.db.deferToCommit(pathtopdf#self.db.table('pfda.proforma').PathPdfProforma,
   #                                proforma_id=proforma_id,
   #                                _deferredId=proforma_id)
   #

   #def pathtopdf(self,record):
   #    if percorso_pdf is None:
   #            record['pathtopdf'] = None
   #    else:    
   #            record['pathtopdf'] = percorso_pdf
        #print(c)
    
            
    def result_handler_pdf(self, resultAttr):

        if not self.results:
            return '{btc_name} completed'.format(btc_name=self.batch_title), dict()
        save_as = slugify(self.print_options.get('save_as') or self.batch_parameters.get('save_as') or '')

        if not save_as:
            if len(self.results)>1:
                save_as = 'multiple_pfda' #slugify(self.batch_title)
            else:
                save_as =  self.page.site.storageNode(self.results['#0']).cleanbasename[9:] 
                #aggiunto [9:] per avere il record -9 caratteri iniziali
        ag_id = self.db.currentEnv.get('current_agency_id')
        tbl_agency =  self.db.table('agz.agency')
        ag_code = tbl_agency.readColumns(columns='code',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        #outputFileNode=self.page.site.storageNode('home:proforma_ranalli', save_as,autocreate=-1)
        outputFileNode=self.page.site.storageNode(f'home:proforma_{ag_code}', save_as,autocreate=-1)
        #outputFileNode=self.page.site.storageNode('home:proforma_ranalli', save_as,autocreate=-1)
        #outputFileNode=self.page.site.storageNode('/home/tommaso/Documenti/Agenzia/PROFORMA', save_as,autocreate=-1)
        #self.print_options.setItem('zipped', True) # settando il valore zipped a True ottengo un file zippato
        zipped =  self.print_options.get('zipped')
        immediate_mode = self.batch_immediate
        if immediate_mode is True:
            immediate_mode = self.batch_parameters.get('immediate_mode')
        if immediate_mode and zipped:
            immediate_mode = 'download'
        if zipped:
            outputFileNode.path +='.zip'
            self.page.site.zipFiles(list(self.results.values()), outputFileNode)
        else:
            outputFileNode.path +='.pdf'
            self.pdf_handler.joinPdf(list(self.results.values()), outputFileNode)
        self.fileurl = outputFileNode.url(nocache=True, download=True)
        inlineurl = outputFileNode.url(nocache=True)
        resultAttr['url'] = self.fileurl
        resultAttr['document_name'] = save_as
        resultAttr['url_print'] = 'javascript:genro.openWindow("%s","%s");' %(inlineurl,save_as)
        if immediate_mode:
            resultAttr['autoDestroy'] = 600
        if immediate_mode=='print':
            self.page.setInClientData(path='gnr.clientprint',value=inlineurl,fired=True)
        elif immediate_mode=='download':
            self.page.setInClientData(path='gnr.downloadurl',value=inlineurl,fired=True)
        
        if outputFileNode:
            
            path_pdf = outputFileNode.internal_path 
        #dal path_pdf del file in stampa verifichiamo la posizione di site in modo che quando preleviamo l'url degli attachments
        #possiamo aggiungere il path iniziale
        pos_site=str.find(path_pdf,"site")

        attcmt=[]
        file_url=[]
        #aggiungiamo agli attachments il file che andiamo a stampare
        attcmt.append(path_pdf)
        #verifichiamo il secondo allegato info port nella tabella fileforemail
        tbl_file =  self.db.table('pfda.fileforemail') #definiamo la variabile della tabella allegati
        att = tbl_file.query(columns="$pathfile", where='$agency_id=:ag_id',ag_id=self.db.currentEnv.get('current_agency_id')).fetch()
        len_att=len(att)
        for r in range(len_att):
            url_allegato=att[r][0]
            #url_att = url_allegato.replace('home:','site/')#cambiamo al url_allegato la posizione home: in site/
            #print(x)
            attcmt.append(url_allegato)#appendiamo agli attcmt l'url_allegato aggiungendoci il path iniziale

        # Lettura degli account email predefiniti all'interno di Agency e Staff
        tbl_staff =  self.db.table('agz.staff')
        account_email,email_mittente,user_fullname = tbl_staff.readColumns(columns='$email_account_id,@email_account_id.address,$fullname',
                  where='$agency_id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        tbl_agency =  self.db.table('agz.agency')
        agency_name,ag_fullstyle,account_emailpec,emailpec_mitt = tbl_agency.readColumns(columns='$agency_name,$fullstyle,$emailpec_account_id, @emailpec_account_id.address',
                  where='$id=:ag_id',
                    ag_id=self.db.currentEnv.get('current_agency_id'))

        email_template_id = self.db.application.getPreference('tpl.template_id',pkg='pfda')
        record_id=list(self.records)[0]
        self.db.table('email.message').newMessageFromUserTemplate(
                                                      record_id=record_id,
                                                      table='pfda.proforma',
                                                      attachments=attcmt,
                                                      account_id = account_email,
                                                      template_id=email_template_id)
        self.db.commit()

    def table_script_options_mail_deliver(self, pane,**kwargs):
        pane.attributes.update(title='!!Deliver mail')
        fb = self.table_script_fboptions(pane)
        self.table_script_option_common(fb,**kwargs)
        fb.textbox(value='^.cc_address', lbl='!!CC', width='100%')
        fb.textbox(value='^.subject', lbl='!!Subject', width='100%')
        fb.simpleTextArea(value='prova', lbl='!!Body', height='8ex', lbl_vertical_align='top')
        tbl_proforma = self.db.table('pfda.proforma')
        

    def dati_proforma(self, record):
        print(x)    
        

    @public_method
    def dati_email(self, record):
        print(x)    
