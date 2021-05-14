from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrbag import Bag

class Main(TableScriptToHtml):

    maintable = 'fatt.fattura'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    virtual_columns = '$notestandard, $serviziextraid'

    doc_header_height = 48
    doc_footer_height = 100
    grid_header_height = 5


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

    def docHeader(self, header):
        layout = header.layout(name='doc_header', margin='5mm', border_width=0)
        
        row = layout.row()
        left_cell = row.cell(width=105)
        #center_cell = row.cell()
        right_cell = row.cell(width=80)

        self.ProformaTestataLeft(left_cell)
        self.ProformaTestataRight(right_cell)
        
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
    
    def gridData(self):
        proforma_id=self.field('serviziextraid')
        result = Bag()
        tbl_proforma = self.db.table('pfda.proforma')
        dati_proforma = tbl_proforma.record(self.record['id']).output('dict')
        tbl_serviziextra = self.db.table('pfda.serviziextra')
        dati_servextra = tbl_serviziextra.record(proforma_id=proforma_id).output('dict')

        if dati_proforma:
            result['dcp'] = Bag(dict(service='Harbour Master Dues', description='', euro=dati_proforma['diritticp']))
            result['admch'] = Bag(dict(service='Administration charge', description='', euro=dati_proforma['admcharge']))
            result['pilot'] = Bag(dict(service='Pilot', description=dati_proforma['notepilot'], euro=dati_proforma['pilot']))
            result['moor'] = Bag(dict(service='Mooringmen', description=dati_proforma['notemoor'], euro=dati_proforma['moor']))
            result['tug'] = Bag(dict(service='Tug', description=dati_proforma['notetug'], euro=dati_proforma['tug']))                           
            result['agency'] = Bag(dict(service='Agency fees', description=dati_proforma['noteagency'], euro=dati_proforma['agency']))
            result['cust'] = Bag(dict(service='Customs clearance', description=dati_proforma['notecustoms'], euro=dati_proforma['customs']))
            result['garbage'] = Bag(dict(service='Garbage', description=dati_proforma['notegarbage'], euro=dati_proforma['garbage']))
            result['retaingarb'] = Bag(dict(service='Dispensation for liquid waste', description=dati_proforma['noteretaingb'], euro=dati_proforma['retaingarbage']))
            result['isps'] = Bag(dict(service='ISPS', description=dati_proforma['noteisps'], euro=dati_proforma['isps']))
            result['misc'] = Bag(dict(service='Miscellaneous', description=dati_proforma['notemisc'], euro=dati_proforma['misc']))
            result['bulk'] = Bag(dict(service='Auth. loading/discharging goods in bulk', description=dati_proforma['notebulk'], euro=dati_proforma['bulkauth']))
        if dati_servextra:
            result['servextra'] = Bag(dict(service=dati_servextra['servizi_id'],
                                            description=dati_servextra['descrizione'],
                                            euro=dati_servextra['tariffa']))    
        return result    
        
         
  
        #select=dict(table='pfda.serviziextra', columns='$servizi_id,$descrizione,$tariffa',
        #                                                where='$id=$serviziextraid')

        #serviziext = self.db.table('pfda.serviziextra').query(columns="""@servizi_id.descrizione as service,$descrizione as descrizione,$tariffa as euro""", where='$id IN :pkeys',
        #                                          pkeys=self.record['selectionPkeys']).fetch()
        

    def gridStruct(self,struct):
        r = struct.view().rows()
        r.cell('service', name='Service')
        r.cell('description', name='Description')
        r.cell('euro', mm_width=20, name='Euro',format='#,###.00')
        #r.cell('')
        #r.fieldcell('servizi_id',mm_width=0, name='Service')
        #r.fieldcell('descrizione',mm_width=0, name='Description')
        #r.fieldcell('tariffa',mm_width=20, name='Euro',format='#,###.00')

    #def gridQueryParameters(self):
    #    return dict(relation='@proforma_servextra')

    def docFooter(self, footer, lastPage=None):
        l = footer.layout('footer',top=1,left=0.5,
                           lbl_class='caption', 
                           content_class = 'footer_content')
                      
        r = l.row(height=8)
        r.cell('Stamps', font_size='8pt')
        r.cell(self.field('stamp'),width=20, font_size='8pt')

                                  
        r = l.row(height=12)
        r.cell(row_border=False)
        #r.cell("Total PFDA", content_class='aligned_right', font_weight= 'bold')
        r.cell(self.field('totalepfda'),lbl='Total pfda Euro',  width=20, font_weight= 'bold')
        r = l.row()
        noteproforma = (self.field('noteproforma')) 
        notestandard = (self.field('notestandard',mask='%s::HTML'))
        r.cell(str(noteproforma) + str(notestandard), content_class='aligned_left', font_size='8pt') 
       