# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('tributicp',pkey='id',name_long='TributiCP',name_plural='tributicp',caption_field='descrizione',lookup=True)
        self.sysFields(tbl)
        tbl.column('descrizione',name_long='Descrizione GT')
        tbl.column('importo',dtype='N',size='10,2',name_long='Importo',format='#,###.00')

    @metadata(mandatory=True)
    def sysRecord_GT_min250(self):
        return self.newrecord(descrizione='<250',importo=31)

    @metadata(mandatory=True)
    def sysRecord_GT_magioreuguale250(self):
        return self.newrecord(descrizione='=>250',importo=62)

    @metadata(mandatory=True)
    def sysRecord_Dangerous(self):
        return self.newrecord(descrizione='Merci pericolose - doppio della tariffa')