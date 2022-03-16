# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        proforma_da = root.branch(u"proforma da", tags="")
        proforma_da.thpage(u"clienti", table="pfda.cliente", tags="", formResource="FormCliente")
        proforma_da.thpage(u"imbarcazione", table="pfda.imbarcazione", tags="")
        proforma_da.thpage(u"proforma", table="pfda.proforma", tags="", viewResource="ViewProforma")
        proforma_da.thpage(u"Tariffe servizi portuali", table="pfda.tariffeportuali", tags="")
        proforma_da.thpage(u"tariffe", table="pfda.tariffe", tags="")
        proforma_da.thpage(u"tariffe_tipo", table="pfda.tariffa_tipo", tags="")
        proforma_da.thpage(u"ormeggiatori", table="pfda.ormeggiatori", tags="")
        proforma_da.thpage(u"agency", table="pfda.agency", tags="")
        proforma_da.thpage(u"servizi", table="pfda.servizi", tags="")
        proforma_da.thpage(u"tug", table="pfda.tug", tags="")
        proforma_da.thpage(u"pilota", table="pfda.pilota", tags="")
        proforma_da.thpage(u"serviziextra", table="pfda.serviziextra", tags="")
        proforma_da.thpage(u"customs", table="pfda.customs", tags="")
        proforma_da.thpage(u"Adm Charge", table="pfda.admcharge", tags="")
        proforma_da.thpage(u"Antifire", table="pfda.antifire", tags="")
        proforma_da.lookups(u"Tabelle Ausiliarie", lookup_manager="pfda")

