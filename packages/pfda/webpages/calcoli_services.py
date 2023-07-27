from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method

class GnrCustomWebPage(object):
    py_requires =  """public:Public,th/th:TableHandler"""

    def main(self, root,**kwargs):
        #rootframe = root.framePane(datapath='main',design='sidebar')
        #rootframe.top.slotToolbar('*,stackButtons,*')
        #tc = rootframe.center.stackContainer(margin='2px')
        pane = root.contentPane(height='100%', margin='15px', border='1px solid silver', datapath='main')
        bc = pane.borderContainer(height='100%',width='100%')
        #top = bc.contentPane(region='top',height='80px')
        #fb = top.formbuilder(cols=10,border_spacing='3px')
        #bc.contentPane(region='right',width='5px')
        #bc.contentPane(region='bottom',height='50px')
        self.pilot(bc.contentPane(title='Calcolo Pilota',
                                                overflow='hidden'))
        self.moor(bc.contentPane(title='Calcolo Ormeggiatori',
                                               overflow='hidden'))
        self.tug(bc.contentPane(title='Calcolo Tug',
                                               overflow='hidden'))
        self.tot(bc.contentPane(title='Calcolo totale',
                                               overflow='hidden'))
        #pane = root.contentPane(height='100%', margin='15px', border='1px solid silver', datapath='main')

        #pane.contentPane(region='center').bagGrid(struct=self.struct_pilot, datapath='.calcolo_pilota',
        #                            width='400px',height='200px', export=True)

    def pilot(self,pane):
        bc = pane.borderContainer(height='200px')
        #rg=bc.roundedGroup(title='Calcolo Pilota',region='center',height='200px').div(margin='10px',margin_left='2px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=2,border_spacing='3px')
        fb.div('<strong>CALCOLO PILOTA</strong>')
        fb.button('clear',fire='.clear_pil')
        bc.dataFormula('.calcolo_pilota.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'dati pilot'})})",_onStart=True,_fired='^.clear_pil')
        bc.contentPane(region='center').bagGrid(struct=self.struct_pilot,datapath='.calcolo_pilota',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)   
   
    def moor(self,pane):
        bc = pane.borderContainer(height='200px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=2,border_spacing='3px')
        fb.div('<strong>CALCOLO MOOR</strong>')
        fb.button('clear',fire='.clear_moor')
        bc.dataFormula('.calcolo_moor.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'dati moor'})})",_onStart=True,_fired='^.clear_moor')
        bc.contentPane(region='center').bagGrid(struct=self.struct_moor,datapath='.calcolo_moor',
                                    width='100%',height='100%', export=True)   
    
    def tug(self,pane):
        bc = pane.borderContainer(height='200px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=2,border_spacing='3px')
        fb.div('<strong>CALCOLO TUG</strong>')
        fb.button('clear',fire='.clear_tug')
        bc.dataFormula('.calcolo_tug.store',"new gnr.GnrBag({r1:new gnr.GnrBag({description:'dati tug'})})",_onStart=True,_fired='^.clear_tug')
        bc.contentPane(region='center').bagGrid(struct=self.struct_tug,datapath='.calcolo_tug',grid_footer='Totals',
                                    width='100%',height='100%', export=True,searchOn=True)   
    
    def tot(self,pane):
        bc = pane.borderContainer(height='200px')
        top = bc.contentPane(region='top',height='30px')
        fb = top.formbuilder(cols=1,border_spacing='3px')
        fb.br()
        fb.numberTextBox('^.total_services',lbl='Total services',lbl_font_weight='bold',font_weight='bold',readOnly=True,format='###,###,###.00')
        fb.dataFormula('.total_services','pilot+moor+tug',pilot='^.calcolo_pilota.grid.sum_pilot',
                       moor='^.calcolo_moor.grid.sum_moor',tug='^.calcolo_tug.grid.sum_tug')

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