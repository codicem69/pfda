# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('tariffeportuali',pkey='id',name_long='tariffeportuali',name_plural='tariffeportuali',caption_field='descrizione')
        self.sysFields(tbl)
        tbl.column('descrizione',name_long='descrizione')
