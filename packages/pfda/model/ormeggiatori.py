# encoding: utf-8
from gnr.core.gnrnumber import decimalRound
from past.utils import old_div

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('ormeggiatori',pkey='id',name_long='ormeggiatori',name_plural='ormeggiatori',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_orm', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffe ormeggiatori').relation('tariffe.id',relation_name='tariffe_orm', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('ovt',dtype='N',size='3',name_long='OVT %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totmoor',dtype='N',size='10,2',name_long='Totale Ormeggiatori',format='#,###.00')

    #def aggiornaOrmeggiatori(self,record):
    #    proforma_id = record['proforma_id']
    #    self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaOrmeggiatori,
    #                                proforma_id=proforma_id,
    #                                _deferredId=proforma_id)
    def aggiornaOrmeggiatori(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServizi,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)

    #def calcolaPrezziRiga(self, record):
    #    prezzo_unitario = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=record['tariffe_id'])
    #    record['pu']=prezzo_unitario
    #    totprest = decimalRound(record['quantita'] * record['pu'] )
    #    ovt = decimalRound(old_div(record['ovt'] * totprest,100))
    #    record['totmoor']=decimalRound(totprest + ovt)
#
    #def trigger_onInserting(self, record):
    #    self.calcolaPrezziRiga(record)
#
    #def trigger_onUpdating(self, record, old_record=None):
    #    self.calcolaPrezziRiga(record)

    def trigger_onInserted(self,record=None):
        self.aggiornaOrmeggiatori(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaOrmeggiatori(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaOrmeggiatori(record)             
