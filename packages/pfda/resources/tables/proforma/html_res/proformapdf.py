 
from gnr.web.gnrbaseclasses import TableScriptToHtml


class Main(TableScriptToHtml):
    #page_width = 210
    #page_height = 297
    maintable = 'pfda.proforma'
    virtual_columns = '$notestandard'
    #Con virtual_columns aggiungo a self.record anche le formulaColumn calcolate che altrimenti di default non verrebbero compilate 
    
    

    def main(self):
        self.Proforma()
        
        #Nel metodo main specifichiamo tutti i metodi da eseguire: in questo caso solo un metodo schedaCliente totalmente customizzato

    def defineCustomStyles(self):
        self.body.style(""".cell_label{
                            font-size:8pt;
                            text-align:left;
                            color:gray;
                            text-indent:1mm;}
    
                            .footer_content{
                            font-size:12pt;
                            font_weight=bold;    
                            text-align:right;
                            margin:2mm;
                            }
                            """)

    def Proforma(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(um='mm',top=1,left=1,right=1, bottom=3,
                                        border_width=0,
                                        font_family='Helvetica',
                                        font_size='9pt',
                                        lbl_height=4,lbl_class='caption')
       

        row = layout.row(height=45)
        left_cell = row.cell(width=105)
        #center_cell = row.cell()
        right_cell = row.cell(width=80)

        self.ProformaTestataLeft(left_cell)
        self.ProformaTestataRight(right_cell)
        griglia_proforma = layout.row( lbl_height=4, lbl_class='smallCaption')
        self.ProformaRighe(griglia_proforma)
        
                             

    def ProformaTestataLeft(self, c):
        l = c.layout('dati_proforma',
                    lbl_class='cell_label',
                    border_width=0)
                
        r = l.row(height=8)
        r.cell(self.field('data'), lbl='Date')
        #r = l.row(height=8)
        r.cell(self.field('protocollo'), lbl='PFDA no.')
        r = l.row(height=8)
        r.cell(self.field('@imbarcazione_id.tipo'), lbl='type') and ' ' and r.cell(self.field('@imbarcazione_id.nome'), lbl='name')
        #r = l.row(height=2)
        #r.cell(self.field('@imbarcazione_id.nome'))
        r = l.row(height=8)
        r.cell(self.field('@imbarcazione_id.bandiera'), lbl='Flag') and ' ' and r.cell(self.field('@imbarcazione_id.loa'), lbl='LOA')
        r = l.row(height=8)
        #r.cell(self.field('@imbarcazione_id.loa'), lbl='LOA')
        #r = l.row(height=8)
        r.cell(self.field('@imbarcazione_id.gt'), lbl='GT') and ' ' and r.cell(self.field('@imbarcazione_id.nt'), lbl='NT')
        #r = l.row(height=8)
        #r.cell(self.field('@imbarcazione_id.nt'), lbl='NT')
        r = l.row(height=8)
        r.cell(self.field('cargo'), lbl='Cargo')
        #r = l.row(height=8)
        #r.cell('Pilot ' + self.field('notepilot') + 'Euro ' + self.field('pilot')) 
        
    def ProformaTestataRight(self, c):
        l = c.layout('dati_cliente', border_width=0)
        
        l.row(height=5).cell('Messrs.', font_weight= 'bold')
        l.row(height=5).cell(self.field('@cliente_id.nome'), font_weight= 'bold')
        l.row(height=5).cell(self.field('@cliente_id.indirizzo'), font_weight= 'bold')
        #comune = self.field('@cliente_id.@comune_id.denominazione')
        #provincia = self.field('@cliente_id.provincia')
        #l.row(height=5).cell('%s (%s)' % (comune, provincia))    

    def ProformaRighe(self, row):
        righeproformaLayout = row.cell().layout(name='datiGrigliaProforma', um='mm',
                                    lbl_height=3,border_color='grey', top=1,left=1,right=1, bottom=3,style='line-height:5mm;text-indent:2mm;')
        intestazione = righeproformaLayout.row(height=6)
        intestazione.cell("Service", width=0, content_class='aligned_center')
        intestazione.cell("description", width=0, content_class='aligned_center')
        intestazione.cell("Euro", width=20, content_class='aligned_center')
        r = righeproformaLayout.row(height=6)
        r.cell("Harbour Master Dues", width=0)
        r.cell("", width=0)
        r.cell(self.field('diritticp'), width=20, content_class='aligned_right') 
        r = righeproformaLayout.row(height=6) 
        r.cell("Administration charge", width=0)
        r.cell("", width=0)
        r.cell(self.field('admcharge'), width=20, content_class='aligned_right')     
        r = righeproformaLayout.row(height=6)
        r.cell("Pilot", width=0)
        r.cell(self.field('notepilot'), width=0)
        r.cell(self.field('pilot'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Mooringmen", width=0)
        r.cell(self.field('notemoor'), width=0)
        r.cell(self.field('moor'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Tug", width=0)
        r.cell(self.field('notetug'), width=0)
        r.cell(self.field('tug'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Agency fees", width=0)
        r.cell(self.field('noteagency'), width=0)
        r.cell(self.field('agency'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Customs clearance", width=0)
        r.cell(self.field('notecustoms'), width=0)
        r.cell(self.field('customs'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Garbage", width=0)
        r.cell(self.field('notegarbage'), width=0)
        r.cell(self.field('garbage'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Dispensation for liquid waste", width=0)
        r.cell(self.field('noteretaingarbage'), width=0)
        r.cell(self.field('retaingarbage'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("ISPS", width=0)
        r.cell(self.field('noteisps'), width=0)
        r.cell(self.field('isps'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Miscellaneous", width=0)
        r.cell(self.field('notemisc'), width=0)
        r.cell(self.field('misc'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Auth. loading/unloading goods in bulk", width=0)
        r.cell(self.field('notebiulk'), width=0)
        r.cell(self.field('bulkauth'), width=20, content_class='aligned_right')

        extraservice = self.record['@proforma_servextra']
        for f in extraservice.values():
            r = righeproformaLayout.row(height=6)
            r.cell(self.toText(f['@servizi_id.descrizione']), width=0)
            r.cell(self.toText(f['descrizione']), width=0)
            #r.cell(self.field(f['tariffa']), width=20, content_class='aligned_right')
            r.cell(self.toText(f['tariffa'], format=self.currencyFormat), width=20, content_class='aligned_right')

        r = righeproformaLayout.row(height=6)
        r.cell("Stamps", width=0)
        r.cell("", width=0)
        r.cell(self.field('stamp'), width=20, content_class='aligned_right')
        r = righeproformaLayout.row(height=6)
        r.cell("Total PFDA", content_class='aligned_right', font_weight= 'bold')
        r.cell(self.field('totalepfda'), width=20, content_class='aligned_right',font_weight= 'bold')    
        
        r = righeproformaLayout.row()
        noteproforma = (self.field('noteproforma')) 
        notestandard = (self.field('notestandard',mask='%s::HTML'))
        r.cell(str(noteproforma) + str(notestandard))
        #r.cell(self.field('noteproforma',mask='%s::HTML') , content_class='aligned_left') 
       # r = righeproformaLayout.row()
        #r.cell(self.field('notestandard',mask='%s::HTML'), content_class='aligned_left')     

   
