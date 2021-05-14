# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('customs',pkey='id',name_long='customs',name_plural='customs',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('proforma_id',size='22',name_long='proforma_id').relation('proforma.id',relation_name='proforma_customs', mode='foreignkey', onDelete='cascade')
        tbl.column('tariffe_id',size='22',name_long='tariffa customs').relation('tariffe.id',relation_name='tariffe_customs', mode='foreignkey', onDelete='raise')
        tbl.column('quantita',dtype='I',name_long='Quantità')
        tbl.column('sconto',dtype='N',size='3',name_long='Sconto %')
        tbl.column('pu', dtype='N', size='10,2', name_long='P.U.',format='#,###.00')
        tbl.column('totcustoms',dtype='N',size='10,2',name_long='Totale customs',format='#,###.00')
