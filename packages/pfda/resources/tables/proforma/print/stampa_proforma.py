 
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Stampa Proforma'

class Main(BaseResourcePrint):
    batch_title = 'Stampa Proforma'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/stampaprof'
    #templates = 'Ranalli_st'

    #Non utilizziamo il table_script_parameters_pane perché ci limiteremo a stampare la selezione corrente
    #def table_script_parameters_pane(self, pane,**kwargs):
    #    fb = pane.formbuilder(cols=1, width='220px')
    #    fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)

    def pre_process(self):
        ag_id = self.db.currentEnv.get('current_agency_id')

        tbl_agency =  self.db.table('agz.agency')
        htmltemplate_id = tbl_agency.readColumns(columns='htmltemplate_id',
                  where='$id=:ag_id',
                    ag_id=ag_id)
        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        carta_intestata = tbl_htmltemplate.readColumns(columns='name',
                            where='$id=:htmltemplate_id', htmltemplate_id=htmltemplate_id)
        #templates = 'Ranalli_st'
        self.templates = carta_intestata
        self.htmlMaker = self.page.site.loadTableScript(page=self.page, table='pfda.proforma',
                                                        respath='html_res/stampaprof', class_name='Main')
