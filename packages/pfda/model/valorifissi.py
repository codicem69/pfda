# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('valorifissi',pkey='id',name_long='valorifissi',name_plural='valorifissi',caption_field='id',lookup=True)
        self.sysFields(tbl)
        tbl.column('garbageval',dtype='N',size='10,2',name_long='Garbage val',format='#,###.00')
        tbl.column('retaingarbval',dtype='N',size='10,2',name_long='Retain Garbage val',format='#,###.00')
        tbl.column('ispsval',dtype='N',size='10,2',name_long='Isps val',format='#,###.00')
        tbl.column('miscval',dtype='N',size='10,2',name_long='Miscellaneous val',format='#,###.00')
        tbl.column('bulkval',dtype='N',size='10,2',name_long='Bulk Auth val',format='#,###.00')
        tbl.column('notemiscval',name_long='Note Miscellaneous val')
