# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('serviziextra',pkey='id',name_long='serviziextra',name_plural='serviziextra',caption_field='servizi_id')
        self.sysFields(tbl)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_servextra', mode='foreignkey', onDelete='cascade')
        tbl.column('servizi_id',size='22',name_long='Servizi').relation('servizi.id',relation_name='servizi_extra', mode='foreignkey', onDelete='raise')
        tbl.column('descrizione',name_long='Descrizione')
        tbl.column('tariffa',dtype='N',size='10',name_long='Tariffa')