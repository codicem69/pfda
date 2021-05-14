#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='pfda package',sqlschema='pfda',sqlprefix=True,
                    name_short='Pfda', name_long='proforma da', name_full='Pfda')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
