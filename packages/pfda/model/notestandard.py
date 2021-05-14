# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('notestandard',pkey='id',name_long='notestandard',name_plural='notestandard',caption_field='descrizione')
        self.sysFields(tbl)
        tbl.column('descrizione',name_long='Descrizione')
