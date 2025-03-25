# encoding: utf-8
from gnr.core.gnrnumber import decimalRound
from gnr.core.gnrlang import GnrException

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('tug',pkey='id',name_long='tug',name_plural='tug',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_tug', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffe tug').relation('tariffe.id',relation_name='tariffe_tug', mode='foreignkey', onDelete='setnull')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('numero_tug',dtype='I',name_long='Numero Tug')
        tbl.column('ovt',dtype='N',size='3',name_long='OVT %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00',defaultFrom='@tariffe_id.valore')
        tbl.column('tottug',dtype='N',size='10,2',name_long='Totale Tug',format='#,###.00')

    def aggiornaTug(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServizi,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)
    #def aggiornaTug(self,record):
    #    proforma_id = record['proforma_id']
    #    self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaTug,
    #                                proforma_id=proforma_id,
    #                                _deferredId=proforma_id)
    #def trigger_onInserting(self, record):
    #    self.aggiornaPilota(record)

    #def trigger_onUpdating(self, record):
    #    self.aggiornaPilota(record)
    def calcolaPrezziRiga(self, record):
        pu = self.db.table('pfda.tariffe').readColumns(columns='$valore',pkey=record['tariffe_id'])
        record['pu'] = pu
        numero_tug = record.get('numero_tug') 
        if numero_tug is None or numero_tug == 0:
            raise GnrException('Inserisci il numero di rimorchiatori')
        numero_prestazioni = record['quantita']
        if numero_prestazioni is None or numero_prestazioni == 0:
            raise GnrException('Inserisci il numero di prestazioni')
        record['tottug'] = decimalRound(record['quantita'] * record['pu']*record['numero_tug']+decimalRound(record.get('quantita')*record.get('numero_tug')*record.get('pu')*(record.get('ovt') if record.get('ovt') else 0)/100))

    def trigger_onInserting(self, record):
        self.calcolaPrezziRiga(record)

    def trigger_onUpdating(self, record, old_record=None):
        self.calcolaPrezziRiga(record)

    def trigger_onInserted(self,record=None):
        self.aggiornaTug(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaTug(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaTug(record) 