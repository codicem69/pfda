from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method

class Main(TableScriptToHtml):

    maintable = 'pfda.proforma'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    #virtual_columns = '$notestandard'

    doc_header_height = 48
    doc_footer_height = 80
    grid_header_height = 5


    def defineCustomStyles(self):
        self.body.style(""".cell_label{
                            font-size 8pt;
                            text-align:left;
                            color:gray;
                            text-indent:1mm;}
    
                            .footer_content{   
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
        r.cell(self.field('data'), lbl='Date', font_size='10pt')
        #r = l.row(height=8)
        r.cell(self.field('protocollo'), lbl='PFDA no.', font_size='10pt')
        r = l.row(height=8)
       # r.cell(self.field('@imbarcazione_id.tipo'), lbl='type') and ' ' and r.cell(self.field('@imbarcazione_id.nome), lbl='name')
        r.cell(self.field('@imbarcazione_id.tipo'), lbl='type', font_size='10pt') and ' ' and r.cell(self.field('@imbarcazione_id.nome'), lbl='name', font_size='10pt')
        #r = l.row(height=2)
        #r.cell(self.field('@imbarcazione_id.nome'))
        r = l.row(height=8)
        r.cell(self.field('@imbarcazione_id.bandiera'), lbl='Flag', font_size='10pt') and ' ' and r.cell(self.field('@imbarcazione_id.loa'), lbl='LOA', font_size='10pt')
        r = l.row(height=8)
        #r.cell(self.field('@imbarcazione_id.loa'), lbl='LOA')
        #r = l.row(height=8)
        r.cell(self.field('@imbarcazione_id.gt'), lbl='GT', font_size='10pt') and ' ' and r.cell(self.field('@imbarcazione_id.nt'), lbl='NT', font_size='10pt')
        #r = l.row(height=8)
        #r.cell(self.field('@imbarcazione_id.nt'), lbl='NT')
        r = l.row(height=8)
        r.cell(self.field('cargo'), lbl='Cargo', font_size='10pt')
        #r = l.row(height=8)
        #r.cell('Pilot ' + self.field('notepilot') + 'Euro ' + self.field('pilot')) 
        
    def ProformaTestataRight(self, c):
        l = c.layout('dati_cliente', border_width=0)
        
        l.row(height=5).cell('Messrs.', font_weight= 'bold')
        l.row(height=10).cell(self.field('@cliente_id.nome'), font_weight= 'bold', font_size='10pt')
        l.row(height=5).cell(self.field('@cliente_id.indirizzo'), font_weight= 'bold', font_size='10pt')
        #comune = self.field('@cliente_id.@comune_id.denominazione')
        #provincia = self.field('@cliente_id.provincia')
        #l.row(height=5).cell('%s (%s)' % (comune, provincia))    


    def gridData(self):
        #proforma_id=self.field('serviziextraid')
        result = Bag()
        tbl_proforma = self.db.table('pfda.proforma')
        dati_proforma = tbl_proforma.record(self.record['id']).output('dict')
        proforma_id = tbl_proforma.record(self.record['id']).output('record')
        #tbl_serviziextra = self.db.table('pfda.serviziextra')
        #dati_servextra = tbl_serviziextra.record(proforma_id=proforma_id).output('dict')
        prof_id = dati_proforma['id']

       #righe = [dict(descrizione_servizio='Harbour Master Dues', descrizione='', tariffa=self.record['diritticp']),
       #         dict(descrizione_servizio='Administration charge', descrizione='',tariffa=self.record['admcharge']),
       #         dict(descrizione_servizio='Pilot', descrizione=self.record['notepilot'],tariffa=self.record['pilot']),
       #         dict(descrizione_servizio='Mooringmen', descrizione=self.record['notemoor'],tariffa=self.record['moor']),
       #         dict(descrizione_servizio='Tug', descrizione=self.record['notetug'],tariffa=self.record['tug']),
       #         dict(descrizione_servizio='Agency fees', descrizione=self.record['noteagency'],tariffa=self.record['agency']),
       #         dict(descrizione_servizio='Customs clearance', descrizione=self.record['notecustoms'],tariffa=self.record['customs']),
       #         dict(descrizione_servizio='Garbage', descrizione=self.record['notegarbage'],tariffa=self.record['garbage']),
       #         dict(descrizione_servizio='Dispensation for liquid waste', descrizione=self.record['noteretaingb'],tariffa=self.record['retaingarbage']),
       #         dict(descrizione_servizio='Isps', descrizione=self.record['noteisps'],tariffa=self.record['isps']),
       #         dict(descrizione_servizio='Miscellaneous', descrizione=self.record['notemisc'],tariffa=self.record['misc']),
       #         dict(descrizione_servizio='Auth. loading/unloading goods in bulk', descrizione=self.record['notebulk'],tariffa=self.record['bulkauth'])]
        
        righe = []
        if self.record['diritticp']:
            righe.append(dict(descrizione_servizio='Harbour Master Dues', descrizione='', tariffa=self.record['diritticp']))
        if self.record['admcharge']:
            righe.append(dict(descrizione_servizio='Administration charge', descrizione='',tariffa=self.record['admcharge']))
        if self.record['pilot'] or self.record['notepilot']:
            righe.append(dict(descrizione_servizio='Pilot', descrizione=self.record['notepilot'],tariffa=self.record['pilot']))
        if self.record['moor'] or self.record['notemoor']:
            righe.append(dict(descrizione_servizio='Mooringmen', descrizione=self.record['notemoor'],tariffa=self.record['moor']))
        if self.record['tug'] or self.record['notetug']:
            righe.append(dict(descrizione_servizio='Tug', descrizione=self.record['notetug'],tariffa=self.record['tug']))
        if self.record['agency'] or self.record['noteagency']:
            righe.append(dict(descrizione_servizio='Agency fees', descrizione=self.record['noteagency'],tariffa=self.record['agency']))
        if self.record['customs'] or self.record['notecustoms']:
            righe.append(dict(descrizione_servizio='Customs clearance', descrizione=self.record['notecustoms'],tariffa=self.record['customs']))    
        if self.record['garbage'] or self.record['notegarbage']:
            righe.append(dict(descrizione_servizio='Garbage', descrizione=self.record['notegarbage'],tariffa=self.record['garbage']))
        if self.record['retaingarbage'] or self.record['noteretaingb']:
            righe.append(dict(descrizione_servizio='Dispensation for liquid waste', descrizione=self.record['noteretaingb'],tariffa=self.record['retaingarbage']))    
        if self.record['isps'] or self.record['noteisps']:
            righe.append(dict(descrizione_servizio='Isps', descrizione=self.record['noteisps'],tariffa=self.record['isps']))    
        if self.record['misc'] or self.record['notemisc']:
            righe.append(dict(descrizione_servizio='Miscellaneous', descrizione=self.record['notemisc'],tariffa=self.record['misc']))
        if self.record['bulkauth'] or self.record['notebulk']:
            righe.append(dict(descrizione_servizio='Auth. loading/unl. goods in bulk', descrizione=self.record['notebulk'],tariffa=self.record['bulkauth']))
        if self.record['antifire'] or self.record['noteantifire']:
            righe.append(dict(descrizione_servizio='Antifire/Antipollution', descrizione=self.record['noteantifire'],tariffa=self.record['antifire']))


        #campi_default = dict(diritticp='Harbour Master Dues',admcharge='Administration charge',pilot='Pilot',agency='Agency fees')
        #for campo,etichetta in campi_default.items():
        #   if self.record[campo]:
        #       righe.append(dict(descrizione_servizio=etichetta, descrizione='', tariffa=self.record[campo]))


        #if dati_proforma:
        #    if not (dati_proforma['diritticp'] is None):
        #        result['dcp'] = Bag(dict(service='Harbour Master Dues', description='', euro=dati_proforma['diritticp']))
        #    if not (dati_proforma['admcharge'] is None):
        #        result['admch'] = Bag(dict(service='Administration charge', description='', euro=dati_proforma['admcharge']))
        #    if not (dati_proforma['pilot'] is None):
        #        result['pilot'] = Bag(dict(service='Pilot', description=dati_proforma['notepilot'], euro=dati_proforma['pilot']))
        #    if not (dati_proforma['moor'] is None):
        #        result['moor'] = Bag(dict(service='Mooringmen', description=dati_proforma['notemoor'], euro=dati_proforma['moor']))
        #    if not (dati_proforma['tug'] is None):
        #        result['tug'] = Bag(dict(service='Tug', description=dati_proforma['notetug'], euro=dati_proforma['tug']))                           
        #    if not (dati_proforma['agency'] is None):
        #        result['agency'] = Bag(dict(service='Agency fees', description=dati_proforma['noteagency'], euro=dati_proforma['agency']))
        #    if not (dati_proforma['customs'] is None):
        #        result['cust'] = Bag(dict(service='Customs clearance', description=dati_proforma['notecustoms'], euro=dati_proforma['customs']))
        #    if not (dati_proforma['garbage'] is None):
        #        result['garbage'] = Bag(dict(service='Garbage', description=dati_proforma['notegarbage'], euro=dati_proforma['garbage']))
        #    if not (dati_proforma['retaingarbage'] is None):
        #        result['retaingarb'] = Bag(dict(service='Dispensation for liquid waste', description=dati_proforma['noteretaingb'], euro=dati_proforma['retaingarbage']))
        #    if not (dati_proforma['isps'] is None):
        #        result['isps'] = Bag(dict(service='ISPS', description=dati_proforma['noteisps'], euro=dati_proforma['isps']))
        #    if not (dati_proforma['misc'] is None):
        #        result['misc'] = Bag(dict(service='Miscellaneous', description=dati_proforma['notemisc'], euro=dati_proforma['misc']))
        #    if not (dati_proforma['bulkauth'] is None):
        #        result['bulk'] = Bag(dict(service='Auth. loading/discharging goods in bulk', description=dati_proforma['notebulk'], euro=dati_proforma['bulkauth']))
        #  

        # dovendo sommare al dizionario delle righe i campi della tabella serviziextra dobbiamo fare in modo che le chiavi dei dati corrispondano
        # per fare questo nella ricerca sottostante abbiamo inserito la query con la ricerca su tutte le colonne selezionando * e aggiungendo il campo 
        # descrizione_servizio che è un campo alias creato sotto la tabella servizi extra al fine di restituire la descrizione del servizio extra
         
        serviziextra = self.db.table('pfda.serviziextra').query(columns='*,$descrizione_servizio',
                                                                    where='$proforma_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        #result = []
        #for r in righe:
        #    if r['tariffa']:
        #        result + r
        #result = result + serviziextra
        #for r in serviziextra:
        #    if serviziextra[r] == "Italian Anchorage Dues":
        #        s='ok'

        righe = righe + serviziextra
       


            #if not (serviziextra is None):
            #    result['serviziextra'] = Bag(self.db.table('pfda.serviziextra').readColumns(columns="""@servizi_id.descrizione AS service, 
            #                                                                    $descrizione AS description,
            #                                                                    $tariffa AS euro""", 
            #                                                                    where='$proforma_id=:p_id',p_id=prof_id))
            #                                                                    .
        #if dati_servextra:
         #   result['servextra'] = Bag(dict(service=dati_servextra['servizi_id'],
          #                                  description=dati_servextra['descrizione'],
           #                                 euro=dati_servextra['tariffa']))    
        return righe

       
         
  
        #select=dict(table='pfda.serviziextra', columns='$servizi_id,$descrizione,$tariffa',
        #                                                where='$id=$serviziextraid')

        #serviziext = self.db.table('pfda.serviziextra').query(columns="""@servizi_id.descrizione as service,$descrizione as descrizione,$tariffa as euro""", where='$id IN :pkeys',
        #                                          pkeys=self.record['selectionPkeys']).fetch()
    def calcRowHeight(self):
        #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
        descr_servizio_offset = 34
        descr_descrizione_offset = 80
        #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
        #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
        #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
        n_rows_nome_service = len(self.rowField('descrizione_servizio'))//descr_servizio_offset + 1
        n_rows_nome_descr = len(self.rowField('descrizione'))//descr_descrizione_offset + 1
        n_rows_nome_tariffa = len(self.rowField('tariffa'))//10 + 1
  #      n_rows_nome_provincia = len(self.rowField('_sigla_provincia_nome'))//nome_offset + 1
        #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
        #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
        n_rows = max(n_rows_nome_service,n_rows_nome_descr,n_rows_nome_tariffa )#, n_rows_nome_provincia)
        height = (self.grid_row_height * n_rows)
        return height



    def gridStruct(self,struct):
        r = struct.view().rows()
        r.cell('descrizione_servizio', name='Service', mm_width=50)
        r.cell('descrizione', name='Description')
        r.cell('tariffa', mm_width=20, name='Euro',format='#,###.00')
        
        #r.cell('prof_id')
        #r.fieldcell('servizi_id',mm_width=0, name='Service')
        #r.fieldcell('descrizione',mm_width=0, name='Description')
        #r.fieldcell('tariffa',mm_width=20, name='Euro',format='#,###.00')

    #def gridQueryParameters(self):
    #    return dict(relation='@proforma_servextra')

    def docFooter(self, footer, lastPage=None):
        righe = []
        serviziextra = self.db.table('pfda.serviziextra').query(columns='*,$descrizione_servizio',
                                                                    where='$proforma_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        righe = righe + serviziextra

        
        if len (righe) != 0:
            for r in righe:
                if r['descrizione_servizio'] == 'Italian Anchorage Dues':
                    descr_tot='Total PFDA Euro'
                else:
                    descr_tot='Total PFDA excluded Italian Anchorage Dues - Euro'
        else:
            descr_tot='Total PFDA excluded Italian Anchorage Dues - Euro'
        
        l = footer.layout('footer',top=1,left=0.5,
                           lbl_class='caption', 
                           content_class = 'footer_content')
        
        r = l.row(height=4)
        r.cell('Stamps',content_class='aligned_right', font_size='8pt')
        r.cell(self.field('stamp'),width=20,content_class='aligned_right', font_size='8pt')                     
        r = l.row(height=6)


        #self.descrizione_tot()

        r.cell(descr_tot,content_class='aligned_right', font_size='12pt', font_weight= 'bold',row_border=False)
        #r.cell('Total PFDA Euro',content_class='aligned_right', font_size='12pt', font_weight= 'bold',row_border=False)
        #r.cell("Total PFDA", content_class='aligned_right', font_weight= 'bold')
        r.cell(self.field('totalepfda'),content_class='aligned_right', width=20, font_weight= 'bold')
        if self.record['timbro'] == True:
            r = l.row(row_border=False)
        else:
            r = l.row()
      
        noteproforma = (self.field('noteproforma')) 
        #notestandard = (self.db.application.getPreference('notestandard',pkg='pfda'), mask=“%s::HTML”)
        note_standard = self.db.application.getPreference('notestandard',pkg='pfda')
        #timbro = self.db.application.getPreference('timbro',pkg='pfda')

        #notestandard = gnr.app_preference.pfda.notestd
        #notestandard = (self.field ('notestandard', mask='%s::HTML'))
        #notestandard = (self.field('notestandard',mask='%s::HTML'))
        #r.cell(note)
        #r.cell(str(noteproforma) + str(notestandard), content_class='aligned_left', font_size='8pt') 
        
        #r.cell(self.db.application.getPreference('notestandard',pkg='pfda'), mask="%s::HTML", content_class='aligned_left', font_size='8pt')
        
        #r.cell(str(noteproforma) + str(self.db.application.getPreference('notestandard',pkg='pfda'), mask="%s::HTML"), content_class='aligned_left', font_size='8pt') 
   
        r.cell(str(noteproforma) + str("{note_standard}::HTML".format(note_standard=note_standard)), content_class='aligned_left', font_size='8pt')

        #timbro="http://127.0.0.1:8083/_storage/site/timbro/image/timbro_societa.png?_pc=821&v_x=94.5&v_y=95&v_z=0.34&v_r=0&v_h=150&v_w=150"
        if self.record['timbro'] == True:
            r = l.row()
            timbro=self.page.externalUrl('_storage/site/timbro/image/timbro_societa.png?_pc=821&v_x=94.5&v_y=95&v_z=0.34&v_r=0&v_h=150&v_w=150')
            #timbro="http://127.0.0.1:8083/_storage/site/timbro/image/timbro_societa.png?_pc=821&v_x=94.5&v_y=95&v_z=0.34&v_r=0&v_h=150&v_w=150"
            r.cell("""<img src="%s" width="100" height="100">::HTML""" %timbro,width=0)
        #print (s)
        #if self.record['noteproforma']:

    def calcDocFooterHeight(self):  
            if self.record['noteproforma']:
            
                return self.doc_header_height + 50
            else:
                return self.doc_footer_height    

        
