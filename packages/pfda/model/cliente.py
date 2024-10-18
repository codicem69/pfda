# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('cliente',pkey='id',name_long='cliente',name_plural='clienti',caption_field='nome')
        self.sysFields(tbl)
        tbl.column('nome',name_long='Ragione Sociale',validate_notnull=True)
        tbl.column('indirizzo',name_long='Indirizzo')
        tbl.column('tel',name_long='Telefono')
        tbl.column('email',name_long='Email')
        tbl.column('email_cc',name_long='Email cc')
        tbl.column('note',name_long="Note")
        tbl.formulaColumn('cliente_full',"$nome || ' - ' || $indirizzo")
