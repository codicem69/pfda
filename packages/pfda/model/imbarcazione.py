# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('imbarcazione',pkey='id',name_long='imbarcazione',name_plural='imbarcazione',caption_field='nome')
        self.sysFields(tbl)
        tbl.column('tipo',size='10',name_long='Tipo')
        tbl.column('nome',name_long='Nome')
        tbl.column('bandiera',name_long='Bandiera')
        tbl.column('loa',name_long='LOA')
        tbl.column('gt',name_long='GT')
        tbl.column('nt',name_long='NT')