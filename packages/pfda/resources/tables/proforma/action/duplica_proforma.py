from gnr.web.batch.btcaction import BaseResourceAction

caption = 'Duplica Proforma'
description = 'Duplica Proforma'

class Main(BaseResourceAction):
    batch_prefix = 'DUPF' # DUPlica Fatture
    batch_title = 'Duplica Proforma'
    batch_cancellable = True
    batch_immediate = True
    batch_delay = 0.5

    def do(self):

        pfda_pkeys = self.get_selection_pkeys()

        for pfda_pkey in self.btc.thermo_wrapper(pfda_pkeys, 'proforma', message='Proforma', maximum=len(pfda_pkeys)):
            self.tblobj.duplica(proforma_id=pfda_pkey)
        # self.db.commit()
