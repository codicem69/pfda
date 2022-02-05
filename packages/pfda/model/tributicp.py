# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('tributicp',pkey='id',name_long='TributiCP',name_plural='tributicp',caption_field='descrizione',lookup=True)
        self.sysFields(tbl)
        tbl.column('descrizione',name_long='Descrizione')
        tbl.column('importo',dtype='N',size='10,2',name_long='Importo',format='#,###.00')
