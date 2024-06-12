from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tip_imbarcazione', pkey='code', name_long='!![en]Vessel type', name_plural='!![en]Vessels type',caption_field='code',lookup=True)
        self.sysFields(tbl,id=False, counter=True)
 
        tbl.column('code',name_long='!![en]Code')        

    @metadata(mandatory=True)
    def sysRecord_mv(self):
        return self.newrecord(code='M/V')
    
    @metadata(mandatory=True)
    def sysRecord_my(self):
        return self.newrecord(code='M/Y')
    
    @metadata(mandatory=True)
    def sysRecord_mt(self):
        return self.newrecord(code='M/T')
    
    @metadata(mandatory=True)
    def sysRecord_mpne(self):
        return self.newrecord(code='M/PNE')
    
    @metadata(mandatory=True)
    def sysRecord_hsc(self):
        return self.newrecord(code='HSC')
    
    @metadata(mandatory=True)
    def sysRecord_mb(self):
        return self.newrecord(code='M/B')
    
    @metadata(mandatory=True)
    def sysRecord_sv(self):
        return self.newrecord(code='S/V')
    
    @metadata(mandatory=True)
    def sysRecord_dredger(self):
        return self.newrecord(code='Dredger')
    