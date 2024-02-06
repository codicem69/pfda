# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('antifire',pkey='id',name_long='antifire',name_plural='antifire',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_antifire', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffe antifire').relation('tariffe.id',relation_name='tariffe_antifire', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('ore',dtype='N',size='3',name_long='n. Ore')
        #tbl.column('ovt',dtype='N',size='3',name_long='OVT %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
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

    def trigger_onInserted(self,record=None):
        self.aggiornaAntifire(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaAntifire(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaAntifire(record) 
