from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method

class GnrCustomWebPage(object):
    py_requires =  """public:Public,th/th:TableHandler"""

    def main(self, root,**kwargs):
        rootframe = root.framePane(datapath='main',design='sidebar')
        rootframe.top.slotToolbar('*,stackButtons,*')
        tc = rootframe.center.stackContainer(margin='2px')

        self.pilot(tc.contentPane(title='Calcolo Pilota',
                                                overflow='hidden'))
        self.moor(tc.contentPane(title='Calcolo Ormeggiatori',
                                                overflow='hidden'))
        self.tug(tc.contentPane(title='Calcolo Tug',
                                                overflow='hidden'))
        #pane = root.contentPane(height='100%', margin='15px', border='1px solid silver', datapath='main')

        #pane.contentPane(region='center').bagGrid(struct=self.struct_pilot, datapath='.calcolo_pilota',
        #                            width='400px',height='200px', export=True)

    def pilot(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_pilota.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'Test variable'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_pilot,datapath='.calcolo_pilota',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)   
    def moor(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_moor.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'Test variable'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_moor,datapath='.calcolo_moor',
                                    width='100%',height='100%', export=True)   
    
    def tug(self,pane):
        bc = pane.borderContainer(height='400px',width='800px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=10,border_spacing='3px')
        fb.button('clear',fire='.clear')
        bc.dataFormula('.calcolo_tug.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'dati pilota'})})",_onStart=True,_fired='^.clear')
        bc.contentPane(region='center').bagGrid(struct=self.struct_tug,datapath='.calcolo_tug',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)   
    
    def struct_pilot(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%pil%', 
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('qt',name='Quantità',dtype='N',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale Pilota',dtype='N',formula='qt*valore+qt*valore*ovt/100',totalize='.sum_pilot',format='###,###,###.00')

    def struct_moor(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%orm%', 
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('qt',name='Quantità',dtype='N',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale Moor',dtype='N',formula='qt*valore+qt*valore*ovt/100',totalize='.sum_moor',format='###,###,###.00')    
        
       
    def struct_tug(self, struct):
        r = struct.view().rows()
        r.cell('tariffa_id',name='Tariffe',width='20em', edit=dict(validate_notnull=True,table='pfda.tariffe',tag='dbSelect',
                                            value='^.tariffa_id',
                                            rowcaption='$codice,$descrizione',
                                            auxColumns='@tariffa_tipo_id.descrizione',
                                            columns='$codice',condition=":cod is NULL OR :cod = '' OR $codice LIKE :cod",
                                            condition_cod='%tug%',
                                            selected_valore='.valore',
                                            hasDownArrow=True))
        r.cell('valore',name='P.U.', dtype='N', size='10,2')
        r.cell('n_tug',name='Numero Tug',dtype='N',size='3',edit=True)
        r.cell('qt',name='Quantità prestazioni',dtype='N',size='3',edit=True)
        r.cell('ovt',name='OVT',dtype='N',size='3',edit=True)
        r.cell('tot',name='Totale TUG',dtype='N',formula='n_tug*valore*qt+n_tug*valore*qt*ovt/100',totalize='.sum_tug',format='###,###,###.00')