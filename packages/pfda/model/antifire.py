# encoding: utf-8
from gnr.core.gnrnumber import decimalRound
from gnr.core.gnrlang import GnrException

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('antifire',pkey='id',name_long='antifire',name_plural='antifire',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_antifire', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffe antifire').relation('tariffe.id',relation_name='tariffe_antifire', mode='foreignkey', onDelete='setnull')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('ore',dtype='N',size='3',name_long='n. Ore')
        #tbl.column('ovt',dtype='N',size='3',name_long='OVT %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00',defaultFrom='@tariffe_id.valore')
        tbl.column('totantifire',dtype='N',size='10,2',name_long='Totale Antifire',format='#,###.00')

    def aggiornaAntifire(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServizi,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)

    #def aggiornaAntifire(self,record):
    #    proforma_id = record['proforma_id']
    #    self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaAntifire,
    #                                proforma_id=proforma_id,
    #                                _deferredId=proforma_id)    

    #def trigger_onInserting(self, record):
    #    self.aggiornaPilota(record)

    #def trigger_onUpdating(self, record):
    #    self.aggiornaPilota(record)
    def calcolaPrezziRiga(self, record):
        pu = self.db.table('pfda.tariffe'
        ).readColumns(columns='$valore',pkey=record['tariffe_id'])
        record['pu'] = pu
        quantita = record.get('quantita') 
        if quantita is None or quantita == 0:
            raise GnrException('Inserisci la quantità')
        ore = record.get('ore') 
        if ore is None or ore == 0:
            raise GnrException('Inserisci le ore')
        
        record['totantifire'] = decimalRound(record['quantita'] * record['ore'] * record['pu']+decimalRound(record.get('quantita')*record.get('ore')*record.get('pu')*(record.get('ovt') if record.get('ovt') else 0)/100))

    def trigger_onInserting(self, record):
        self.calcolaPrezziRiga(record)

    def trigger_onUpdating(self, record, old_record=None):
        self.calcolaPrezziRiga(record)
        
    def trigger_onInserted(self,record=None):
        self.aggiornaAntifire(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaAntifire(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaAntifire(record) 
