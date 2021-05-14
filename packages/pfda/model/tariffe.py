# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('tariffe',pkey='id',name_long='tariffe',name_plural='tariffe',caption_field='descrizione')
        self.sysFields(tbl)
        tbl.column('codice',name_long='Codice')
        tbl.column('descrizione',name_long='Descrizione')
        tbl.column('valore',dtype='N',name_long='Valore',format='#,###.00')
        tbl.column('tariffa_tipo_id',size='22',name_long='tariffe').relation('tariffa_tipo.id',relation_name='tariffe', mode='foreignkey', onDelete='raise')