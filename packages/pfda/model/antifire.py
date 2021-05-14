# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('antifire',pkey='id',name_long='antifire',name_plural='antifire',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_antifire', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffe antifire').relation('tariffe.id',relation_name='tariffe_antifire', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('ore',dtype='N',size='3',name_long='n. Ore')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totantifire',dtype='N',size='10,2',name_long='Totale Tug',format='#,###.00')