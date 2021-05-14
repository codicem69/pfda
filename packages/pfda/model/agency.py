# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('agency',pkey='id',name_long='agency',name_plural='agency',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_agency', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffa agency').relation('tariffe.id',relation_name='tariffe_agency', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('sconto',dtype='N',size='3',name_long='Sconto %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totagency',dtype='N',size='10,2',name_long='Totale Agency',format='#,###.00')
