# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('imbarcazione',pkey='id',name_long='imbarcazione',name_plural='imbarcazione',caption_field='nome')
        self.sysFields(tbl)
        #tbl.column('tipo',name_long='Tipo')
        tbl.column('tip_imbarcazione_code', group='_', name_long='!![en]Vessel type',batch_assign=dict(hasDownArrow=True)
                    ).relation('tip_imbarcazione.code', relation_name='', mode='foreignkey', onDelete='raise')
        tbl.column('nome',name_long='Nome', validate_case='u')
        tbl.column('bandiera',name_long='Bandiera')
        tbl.column('flag',size='2',name_long='!![en]Flag').relation('unlocode.nazione.code',relation_name='flag_pfda', mode='foreignkey', onDelete='raise')
        tbl.column('loa',name_long='LOA')
        tbl.column('gt',name_long='GT')
        tbl.column('nt',name_long='NT')
