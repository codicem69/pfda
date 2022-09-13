class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('fileforemail',pkey='id',name_long='fileforemail',name_plural='fileforemail',caption_field='description')
        self.sysFields(tbl)

        tbl.column('description', name_short='description')
        tbl.column('pathfile', name_short='pathfile')