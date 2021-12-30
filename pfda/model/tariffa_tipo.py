# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('tariffa_tipo',pkey='id',name_long='tariffa_tipo',name_plural='tariffe_tipo',
                        caption_field='hierarchical_descrizione')
        self.sysFields(tbl,hierarchical='descrizione', counter=True, df=True)
        tbl.column('descrizione',name_long='Descrizione')
