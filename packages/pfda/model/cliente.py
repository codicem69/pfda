# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('cliente',pkey='id',name_long='cliente',name_plural='clienti',caption_field='nome')
        self.sysFields(tbl)
        tbl.column('nome',name_long='Ragione Sociale')
        tbl.column('indirizzo',name_long='Indirizzo')
        tbl.column('tel',name_long='Telefono')
        tbl.column('email',name_long='Email')