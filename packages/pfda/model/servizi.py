# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('servizi',pkey='id',name_long='servizi',name_plural='servizi',caption_field='descrizione')
        self.sysFields(tbl)
        tbl.column('descrizione',name_long='Descrizione')