# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('admcharge',pkey='id',name_long='administration charge',name_plural='administration charges',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_admcharge', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffa admcharge').relation('tariffe.id',relation_name='tariffe_admncharge', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totadmcharge',dtype='N',size='10,2',name_long='Totale Adm Charge',format='#,###.00')

    def aggiornaAdmcharge(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServizi,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)
    #def aggiornaAdmcharge(self,record):
    #    proforma_id = record['proforma_id']
    #    self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaAdmcharge,
    #                                proforma_id=proforma_id,
    #                                _deferredId=proforma_id)

    def trigger_onInserted(self,record=None):
        self.aggiornaAdmcharge(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaAdmcharge(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaAdmcharge(record)     