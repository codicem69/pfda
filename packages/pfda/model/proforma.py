# encoding: utf-8
from gnr.core.gnrdecorator import metadata
from gnr.core.gnrnumber import floatToDecimal,decimalRound

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
        tbl.column('diritticp',dtype='N',size='10,2',name_long='Tributi CP',format='#,###.00')
        tbl.column('admcharge',dtype='N',size='10,2',name_long='Administration Charge',format='#,###.00')
        tbl.column('stamp',dtype='N',size='10,2',name_long='Tax Stamps',format='#,###.00')
        tbl.column('totalepfda',dtype='N',size='10,2',name_long='Totale pfda',format='#,###.00')
        tbl.column('noteproforma',name_long='Note Proforma')
        tbl.aliasColumn('bandiera', '@imbarcazione_id.bandiera', name_long='Bandiera')
        tbl.aliasColumn('loa', '@imbarcazione_id.loa', name_long='Loa')
        tbl.aliasColumn('gt', '@imbarcazione_id.gt', name_long='GT')
        tbl.aliasColumn('nt', '@imbarcazione_id.nt', name_long='NT')
        tbl.formulaColumn('garbageval',select=dict(table='pfda.valorifissi',columns='$garbageval',
                                                    where='$id=$id'),
                                                   dtype='N', size='10,2',format='#,###.00')
        tbl.formulaColumn('notestandard',select=dict(table='pfda.notestandard', columns='$descrizione',
                                                        where='$id=$id'))
        tbl.formulaColumn('serviziextraid',select=dict(table='pfda.serviziextra', columns='$proforma_id',
                                                        where='$id=$id'))                                                        
                                                        
   
    def defaultValues(self):
        return dict(data = self.db.workdate)

    def counter_protocollo(self,record=None):
        #F14/000001
        return dict(format='$K$YY/$NNNNNN',code='PFDA',period='YY',
                    date_field='data',showOnLoad=True,recycle=True)        
   
    def ricalcolaOrmeggiatori(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_ormeggiatori = self.db.table('pfda.ormeggiatori').readColumns(columns="""SUM($totmoor) AS totale_ormeggiatori""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_ormeggiatori is None:
                record['moor'] = None
            else:    
                record['moor'] = floatToDecimal(totale_ormeggiatori + 2 or 0) 
            
    def ricalcolaPilota(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_pilota = self.db.table('pfda.pilota').readColumns(columns="""SUM($totpilot) AS totale_pilota""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            
            if totale_pilota is None:
                record['pilot'] = None
            else:    
                record['pilot'] = floatToDecimal(totale_pilota + 2 or 0) 

    def ricalcolaTug(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_tug = self.db.table('pfda.tug').readColumns(columns="""SUM($tottug) AS totale_tug""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_tug is None:
                record['tug'] = None
            else:    
                record['tug'] = floatToDecimal(totale_tug + 2 or 0) 

    def ricalcolaAdmcharge(self,proforma_id=None):
        with self.recordToUpdate(proforma_id) as record:
            totale_admcharge = self.db.table('pfda.admcharge').readColumns(columns="""SUM($totadmcharge) AS totale_admcharge""",
                                                                     where='$proforma_id=:f_id',f_id=proforma_id)
            if totale_admcharge is None:
                record['admcharge'] = None
            else:    
                record['admcharge'] = floatToDecimal(totale_admcharge or 0)                         
            
    