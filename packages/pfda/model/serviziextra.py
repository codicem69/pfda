# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('serviziextra',pkey='id',name_long='serviziextra',name_plural='serviziextra',caption_field='servizi_id')
        self.sysFields(tbl)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_servextra', mode='foreignkey', onDelete='cascade')
        tbl.column('servizi_id',size='22',name_long='Servizi').relation('servizi.id',relation_name='servizi_extra', mode='foreignkey', onDelete='raise')
        tbl.column('descrizione',name_long='Descrizione')
        tbl.column('tariffa',dtype='N',size='10,2',name_long='Tariffa',format='#,###.00')
        tbl.aliasColumn('descrizione_servizio','@servizi_id.descrizione')
        tbl.formulaColumn('servizio_extra',"@servizi_id.descrizione || ' ' || coalesce($descrizione, '') || ' € ' || $tariffa", dtype='T')
        tbl.formulaColumn('serv_extra',"@servizi_id.descrizione || ' ' || coalesce($descrizione, '')")

    def aggiornaServExtra(self,record):
        proforma_id = record['proforma_id']
        self.db.deferToCommit(self.db.table('pfda.proforma').ricalcolaServExtra,
                                    proforma_id=proforma_id,
                                    _deferredId=proforma_id)

    #def trigger_onInserting(self, record):
    #    self.aggiornaPilota(record)

    #def trigger_onUpdating(self, record):
    #    self.aggiornaPilota(record)

    def trigger_onInserted(self,record=None):
        self.aggiornaServExtra(record)

    def trigger_onUpdated(self,record=None,old_record=None):
        self.aggiornaServExtra(record)

    def trigger_onDeleted(self,record=None):
        if self.currentTrigger.parent:
            return
        self.aggiornaServExtra(record) 
