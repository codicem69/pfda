# encoding: utf-8
from gnr.core.gnrdecorator import metadata
from gnr.core.gnrnumber import floatToDecimal,decimalRound
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('proforma',pkey='id',name_long='proforma',name_plural='proforma',caption_field='protocollo')
        self.sysFields(tbl)
        tbl.column('protocollo',size='14',name_long='Protocollo')
        tbl.column('data',dtype='D',name_long='Data')
        tbl.column('cliente_id',size='22',name_long='Cliente').relation('cliente.id',relation_name='cliente', mode='foreignkey', onDelete='raise')
        tbl.column('imbarcazione_id',size='22',name_long='Imbarcazione').relation('imbarcazione.id',relation_name='proforma_imb', mode='foreignkey', onDelete='raise')
        tbl.column('cargo',name_long='Cargo')
        tbl.column('pilot',dtype='N',size='10,2',name_long='Pilot',format='#,###.00')
        tbl.column('notepilot',name_long='Note Pilot')
        tbl.column('moor',dtype='N',size='10,2',name_long='Mooringmen',format='#,###.00')
        tbl.column('notemoor',name_long='Note Moor')
        tbl.column('tug',dtype='N',size='10,2',name_long='Tug',format='#,###.00')
        tbl.column('notetug',name_long='Note Tug')
        tbl.column('agency',dtype='N',size='10,2',name_long='Agency fees',format='#,###.00')
        tbl.column('noteagency',name_long='Note Agency')
        tbl.column('customs',dtype='N',size='10,2',name_long='Customs Clearance',format='#,###.00')
        tbl.column('notecustoms',name_long='Note Customs')
        tbl.column('garbage',dtype='N',size='10,2',name_long='Garbage',format='#,###.00')
        tbl.column('notegarbage',name_long='Note Garbage')
        tbl.column('retaingarbage',dtype='N',size='10,2',name_long='Garbage auth.',format='#,###.00')
        tbl.column('noteretaingb',name_long='Note retain garbage')
        tbl.column('isps',dtype='N',size='10,2',name_long='ISPS',format='#,###.00')
        tbl.column('noteisps',name_long='Note Isps')
        tbl.column('misc',dtype='N',size='10,2',name_long='Miscellaneous',format='#,###.00')
        tbl.column('notemisc',name_long='Note misc')
        tbl.column('bulkauth',dtype='N',size='10,2',name_long='Bulk auth.',format='#,###.00')
        tbl.column('notebulk',name_long='Note bulk auth')
        tbl.column('antifire',dtype='N',size='10,2',name_long='Antifire',format='#,###.00')
        tbl.column('noteantifire',name_long='Note Antifire')
        tbl.column('tot_servextra',dtype='N',size='10,2',name_long='Tot.Serv.Extra',format='#,###.00')
        tbl.column('diritticp',dtype='N',size='10,2',name_long='Tributi CP',format='#,###.00')
        tbl.column('admcharge',dtype='N',size='10,2',name_long='Administration Charge',format='#,###.00')
        tbl.column('stamp',dtype='N',size='10,2',name_long='Tax Stamps',format='#,###.00')
        tbl.column('totalepfda',dtype='N',size='10,2',name_long='Totale pfda',format='#,###.00')
        tbl.column('noteproforma',name_long='Note Proforma')
        tbl.column('pathtopdf',name_long='pathtopdf')
        tbl.column('timbro',dtype='B', name_long='timbro')
        tbl.pyColumn('privacy',name_long='!![en]Privacy email', static=True, dtype='T')
        tbl.pyColumn('servizi',name_long='Servizi proforma', dtype='X')
        tbl.pyColumn('test',name_long='test', dtype='X')
        tbl.aliasColumn('bandiera', '@imbarcazione_id.bandiera', name_long='Bandiera')
        tbl.aliasColumn('loa', '@imbarcazione_id.loa', name_long='Loa')
        tbl.aliasColumn('gt', '@imbarcazione_id.gt', name_long='GT')
        tbl.aliasColumn('nt', '@imbarcazione_id.nt', name_long='NT')

        #tbl.formulaColumn('garbageval',select=dict(table='pfda.valorifissi',columns='$garbageval',
        #                                            where='$id=$id'),
        #                                           dtype='N', size='10,2',format='#,###.00')
        tbl.formulaColumn('notestandard',select=dict(table='pfda.notestandard', columns='$descrizione',
                                                        where=''))#'$id=$id'))

                                                        
    def pyColumn_privacy(self,record,field):
        privacy_email = self.db.application.getPreference('privacy_email',pkg='pfda')
        return privacy_email 

    def pyColumn_servizi(self,record,field):
        
        righe = []
        if record['diritticp']:
            righe.append(dict(descrizione_servizio='Harbour Master Dues', descrizione='', tariffa=record['diritticp']))
        if record['admcharge']:
            righe.append(dict(descrizione_servizio='Administration charge', descrizione='',tariffa=record['admcharge']))
        if record['pilot']:
            righe.append(dict(descrizione_servizio='Pilot', descrizione='',tariffa=record['pilot']))
        elif record['notepilot']: 
            righe.append(dict(descrizione_servizio='Pilot', descrizione=record['notepilot'],tariffa=record['pilot']))   
        if record['moor']:
            righe.append(dict(descrizione_servizio='Mooringmen', descrizione='',tariffa=record['moor']))
        elif record['notemoor']:
            righe.append(dict(descrizione_servizio='Mooringmen', descrizione=record['notemoor'],tariffa=record['moor']))
        if record['tug']:
            righe.append(dict(descrizione_servizio='Tug', descrizione='',tariffa=record['tug']))
        elif record['notetug']:
            righe.append(dict(descrizione_servizio='Tug', descrizione=record['notetug'],tariffa=record['tug']))
        if record['agency']:
            righe.append(dict(descrizione_servizio='Agency fees', descrizione='',tariffa=record['agency']))
        elif record['noteagency']:
            righe.append(dict(descrizione_servizio='Agency fees', descrizione=record['noteagency'],tariffa=record['agency']))
        if record['customs']:
            righe.append(dict(descrizione_servizio='Customs clearance', descrizione='',tariffa=record['customs']))    
        elif record['notecustoms']:
             righe.append(dict(descrizione_servizio='Customs clearance', descrizione=record['notecustoms'],tariffa=record['customs']))    
        if record['garbage']:
            righe.append(dict(descrizione_servizio='Garbage', descrizione='',tariffa=record['garbage']))
        elif record['notegarbage']:
            righe.append(dict(descrizione_servizio='Garbage', descrizione=record['notegarbage'],tariffa=record['garbage']))
        if record['retaingarbage']:
            righe.append(dict(descrizione_servizio='Dispensation for liquid waste', descrizione='',tariffa=record['retaingarbage']))    
        elif record['noteretaingb']:
            righe.append(dict(descrizione_servizio='Dispensation for liquid waste', descrizione=record['noteretaingb'],tariffa=record['retaingarbage']))    
        if record['isps']:
            righe.append(dict(descrizione_servizio='Isps', descrizione='',tariffa=record['isps']))    
        elif record['noteisps']:
            righe.append(dict(descrizione_servizio='Isps', descrizione=record['noteisps'],tariffa=record['isps']))    
        if record['misc']:
            righe.append(dict(descrizione_servizio='Miscellaneous', descrizione='',tariffa=record['misc']))
        elif record['notemisc']:
            righe.append(dict(descrizione_servizio='Miscellaneous', descrizione=record['notemisc'],tariffa=record['misc']))
        if record['bulkauth']:
            righe.append(dict(descrizione_servizio='Auth. loading/unl. goods in bulk', descrizione='',tariffa=record['bulkauth']))
        elif record['notebulk']:
            righe.append(dict(descrizione_servizio='Auth. loading/unl. goods in bulk', descrizione=record['notebulk'],tariffa=record['bulkauth']))
        if record['antifire']:
            righe.append(dict(descrizione_servizio='Antifire/Antipollution', descrizione='',tariffa=record['antifire']))
        elif record['noteantifire']:
            righe.append(dict(descrizione_servizio='Antifire/Antipollution', descrizione=record['noteantifire'],tariffa=record['antifire']))

        serviziextra = self.db.table('pfda.serviziextra').query(columns='$descrizione_servizio,$descrizione,$tariffa',
                                                                    where='$proforma_id=:p_id',
                                                                    p_id=record['id']).fetch()
        serv_ex = len(serviziextra)
        rigaextra=[]
        for n in serviziextra: 
            rigaextra=righe.append(dict(descrizione_servizio=serviziextra[0][0], descrizione=serviziextra[0][1],tariffa=serviziextra[0][2]))
        print(x)
        return righe

    def pyColumn_test(self,record,field):
        tbl_proforma = self.db.table('pfda.proforma')
        dati_proforma = tbl_proforma.record(record['id']).output('dict')
        
        servizio=Bag()
        servizio['pilota.descrizione']='pilota'
        servizio.addItem('pilota.descrizione','pilota2')
        servizio['pilota.note']='in/out'
        servizio['pilota.importo']=250
        servizio['moor.descrizione']='mooringmen'
        servizio['moor.note']='in/out'
        servizio['moor.importo']=750.00
        return servizio
        
    def defaultValues(self,record=None):
        return dict(data = self.db.workdate,
                    garbage=self.db.application.getPreference('garbage_df',pkg='pfda'),
                    retaingarbage=self.db.application.getPreference('retaingarbage_df',pkg='pfda'),
                    isps=self.db.application.getPreference('isps_df',pkg='pfda'),
                    misc=self.db.application.getPreference('misc_df',pkg='pfda'),
                    notemisc=self.db.application.getPreference('notemisc_df',pkg='pfda'),
                    bulkauth=self.db.application.getPreference('bulkauth_df',pkg='pfda'),
                    )
        

    def counter_protocollo(self,record=None):
        #F14/000001
        return dict(format='$K$YY/$NNNNNNN',code='PFDA',period='YY',
                    date_field='data',showOnLoad=True,recycle=True)
                    
                

    
    def ricalcolaOrmeggiatori(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_ormeggiatori = self.db.table('pfda.ormeggiatori').readColumns(columns="""SUM($totmoor) AS totale_ormeggiatori""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_ormeggiatori is None:
                record['moor'] = None
            else:    
                record['moor'] = floatToDecimal(totale_ormeggiatori + 2 or 0) 
                
        self.ricalcolaTotalePfda(proforma_id)
                                                                                       
            
    def ricalcolaPilota(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_pilota = self.db.table('pfda.pilota').readColumns(columns="""SUM($totpilot) AS totale_pilota""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            
            if totale_pilota is None:
                record['pilot'] = None
            else:    
                record['pilot'] = floatToDecimal(totale_pilota + 2 or 0) 
        self.ricalcolaTotalePfda(proforma_id)

    def ricalcolaTug(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_tug = self.db.table('pfda.tug').readColumns(columns="""SUM($tottug) AS totale_tug""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_tug is None:
                record['tug'] = None
            else:    
                record['tug'] = floatToDecimal(totale_tug + 2 or 0) 
        self.ricalcolaTotalePfda(proforma_id)

    def ricalcolaAdmcharge(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_admcharge = self.db.table('pfda.admcharge').readColumns(columns="""SUM($totadmcharge) AS totale_admcharge""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_admcharge is None:
                record['admcharge'] = None
            else:    
                record['admcharge'] = floatToDecimal(totale_admcharge or 0)     
        self.ricalcolaTotalePfda(proforma_id)

    def ricalcolaServExtra(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_serviziextra = self.db.table('pfda.serviziextra').readColumns(columns="""SUM($tariffa) AS tot_servextra""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_serviziextra is None:
                record['tot_servextra'] = None
            else:    
                record['tot_servextra'] = floatToDecimal(totale_serviziextra or 0)
        self.ricalcolaTotalePfda(proforma_id)

    def ricalcolaAntifire(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_antifire = self.db.table('pfda.antifire').readColumns(columns="""SUM($totantifire) AS totantifire""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_antifire is None:
                record['antifire'] = None
            else:    
                record['antifire'] = floatToDecimal(totale_antifire + 2 or 0)                     
        self.ricalcolaTotalePfda(proforma_id)

    def ricalcolaTotalePfda(self,proforma_id):
        with self.recordToUpdate(proforma_id) as record:
            #totale_pfda = self.db.table('pfda.proforma').readColumns(columns="""SUM($pilot+$moor+$tug+$agency+$customs+$garbage+$retaingarbage+$isps+$misc+$bulkauth+$antifire+$tot_servextra+$diritticp+$admcharge+$stamp) AS tot_pfda""",
            #                                                            where='$id=:p_id',p_id=proforma_id)
            #totale_pfda = self.db.table('pfda.proforma').readColumns(columns="""(coalesce($moor))+(coalesce($pilot))+$isps+$tot_servextra AS tot_pfda""",
            #                                                            where='$id=:p_id',p_id=proforma_id)
            if record['pilot'] is None:
                pilot = 0
            else:
                pilot = record['pilot']
            if record['moor'] is None:
                moor = 0
            else:
                moor = record['moor']     
            if record['tug'] is None:
                tug = 0
            else:
                tug = record['tug']  
            if record['agency'] is None:
                agency = 0
            else:
                agency = record['agency']
            if record['customs'] is None:
                customs = 0
            else:
                customs = record['customs']
            if record['garbage'] is None:
                garbage = 0
            else:
                garbage = record['garbage']      
            if record['retaingarbage'] is None:
                retaingarbage = 0
            else:
                retaingarbage = record['retaingarbage']
            if record['isps'] is None:
                isps = 0
            else:
                isps = record['isps']  
            if record['misc'] is None:
                misc = 0
            else:
                misc = record['misc']
            if record['bulkauth'] is None:
                bulkauth = 0
            else:
                bulkauth = record['bulkauth']
            if record['antifire'] is None:
                antifire = 0
            else:
                antifire = record['antifire']
            if record['tot_servextra'] is None:
                tot_servextra = 0
            else:
                tot_servextra = record['tot_servextra']                    
            if record['diritticp'] is None:
                diritticp = 0
            else:
                diritticp = record['diritticp']  
            if record['admcharge'] is None:
                admcharge = 0
            else:
                admcharge = record['admcharge']  
            if record['stamp'] is None:
                stamp = 0
            else:
                stamp = record['stamp']  



            record['totalepfda'] = floatToDecimal(pilot+moor+tug+agency+customs+garbage+retaingarbage+isps+misc+bulkauth+antifire+tot_servextra+diritticp+admcharge+stamp)
            self.db.commit()
            #print(c)

    def aggiornaPdf_onupdating(self,record):
        proforma_id = record['id']
        prot_proforma = record['protocollo']
        prot_proforma = prot_proforma.replace("/", "")
        #print(x)
        nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_proforma[:-1]))#record[0:])
            
        if nome_file is None:
                record['pathtopdf'] = None
        else:    
                record['pathtopdf'] = nome_file
    
    def aggiornaPdf(self,record):
        proforma_id = record['id']
        prot_proforma = record['protocollo']
        
        prot_proforma = prot_proforma.replace("/", "")
        nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_proforma[0:]))#record[0:])
           
        if nome_file is None:
                record['pathtopdf'] = None
        else:    
                record['pathtopdf'] = nome_file

    def aggiorna_Pdf(self,record):
        proforma_id = record['id']
        
        self.db.deferToCommit(self.pdfpath,
                                   proforma_id=proforma_id,
                                   _deferredId=proforma_id)
        
        
    
   

    def trigger_onInserting(self, record):
        #rec=self.checkPkey(record)
      #   print(x)
        self.trigger_assignCounters(record=record)
        self.aggiornaPdf(record)

    def trigger_onUpdating(self, record,old_record=None):
        self.checkPkey(record)
        self.aggiornaPdf(record)

    #def trigger_onInserted(self,record=None):
    #  self.aggiorna_Pdf(record)

    #def trigger_onUpdated(self,record=None,old_record=None):
     # self.aggiornaPdf(record)

    #def trigger_onDeleted(self,record=None):
    #  if self.currentTrigger.parent:
    #      return
    #  self.aggiornaPdf(record)      


    def pdfpath(self,proforma_id=None, record=None):
        
        with self.recordToUpdate(proforma_id) as record:
            prot_proforma = record['protocollo']
            prot_proforma = prot_proforma.replace("/", "")
            nome_file = str.lower('{cl_id}.pdf'.format(
                    cl_id=prot_proforma[:-1]))#record[0:])
            
            if nome_file is None:
                record['pathtopdf'] = None
            else:    
                record['pathtopdf'] = nome_file
        
