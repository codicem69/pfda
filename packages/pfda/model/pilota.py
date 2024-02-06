# encoding: utf-8
from gnr.core.gnrnumber import decimalRound
from past.utils import old_div

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('pilota',pkey='id',name_long='pilota',name_plural='pilota',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_pilota', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffa pilota').relation('tariffe.id',relation_name='tariffe_pilota', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('ovt',dtype='N',size='3',name_long='OVT %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totpilot',dtype='N',size='10,2',name_long='Totale pilota',format='#,###.00')

    def aggiornaPilota(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServizi,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)
    #def aggiornaPilota(self,record):
    #    proforma_id = record['proforma_id']
    #    self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaPilota,
    #                                proforma_id=proforma_id,
    #                                _deferredId=proforma_id)    

    #def calcolaPrezziRiga(self, record):
    #    prezzo_unitario = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=record['tariffe_id'])
    #    record['pu']=prezzo_unitario
    #    totprest = decimalRound(record['quantita'] * record['pu'] )
    #    ovt = decimalRound(old_div(record['ovt'] * totprest,100))
    #    record['totpilot']=decimalRound(totprest + ovt)
#
    #def trigger_onInserting(self, record):
    #    self.calcolaPrezziRiga(record)
#
    #def trigger_onUpdating(self, record, old_record=None):
    #    self.calcolaPrezziRiga(record)

    def trigger_onInserted(self,record=None):
        self.aggiornaPilota(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaPilota(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaPilota(record)                                    
