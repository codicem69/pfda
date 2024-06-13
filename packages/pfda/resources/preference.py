# preference.py
from gnr.core.gnrdecorator import public_method
import os

class AppPref(object):

    def prefpane_pfda(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        #self.costi_fissi(tc.borderContainer(title='!!Costi fissi'))
        self.dati(tc.borderContainer(title='!!Dati'))
    #def costi_fissi(self,pane):    
    #    #pane = parent.contentPane(**kwargs)
    #    fb = pane.formbuilder(cols=2, border_spacing='4px')
#
    #    # Nei **kwargs c'è già il livello di path dati corretto
    #    fb.numbertextbox('^.garbage_df', lbl='costo standard garbage',format='#,###.00') 
    #    fb.numbertextbox('^.retaingarbage_df', lbl='costo standard deroga garbage',format='#,###.00')
    #    fb.numbertextbox('^.isps_df', lbl='costo standard isps',format='#,###.00')
    #    fb.numbertextbox('^.misc_df', lbl='costo standard miscellaneous',format='#,###.00')
    #    fb.textbox('^.notemisc_df', lbl='note standard miscellaneous', width='60em', colspan=2)
    #    fb.numbertextbox('^.bulkauth_df', lbl='costo standard aut. rinfusa',format='#,###.00')
    #    fb.br()
    #    fb.simpleTextArea('^.notestandard',lbl='Note Standard',width='60em', height='200px',editor=True, colspan=2)
    #    fb.br()
    def dati(self,pane):
        fb = pane.formbuilder(cols=2, border_spacing='4px')   
        fb.br()
        fb.dbSelect(value='^.mail.account_id', lbl='Mail account', table='email.account',columns='$',auxColumns='$full_name', hasDownArrow=True)
        fb.dbSelect(value='^.tpl.template_id', lbl='Template',
                        table='adm.userobject', hasDownArrow=True, condition='$objtype=:tpl', condition_tpl='template',
                        rowcaption='$code,$description', auxColumns='$description,$userid', selected_tbl='^.tpl.tbl')
        fb.br()
        fb.div('', width='100em', colspan=2)
        fb.simpleTextArea('^.privacy_email',lbl='Email Privacy',width='100em', height='200px',editor=True)                
        fb.img(src='^.timbro',lbl='Timbro',
                    border='2px dotted silver',
                    crop_width='150px',
                    crop_height='150px',
                    edit=True,
                    placeholder=True,
                    upload_filename='timbro_societa',
                    upload_folder='site:timbro/image')

        
    @public_method
    def onUploaded_file_uploader(self, file_path=None, **kwargs):
        fileSn = self.site.storageNode(file_path)
        fullpath = fileSn.internal_path
        self.setInClientData(value=fullpath, path='main.record.data.pfda.file_path')
        #self.setInClientData(value=file_url, path='main.record.data.pfda.file_url')
        
        self.clientPublish('floating_message', message='Upload completed')

    @public_method
    def uploadFile(self, file_path=None, **kwargs):
        fileSn = self.site.storageNode(file_path)
        file_url = fileSn.url()
        fullpath = fileSn.internal_path
        print(fullpath)
        #file_size = os.path.getsize(fullpath) / 1024
        #self.setInClientData(value=file_size, path='test.test_1_dropUploaderWithMethod.size')
        self.setInClientData(value=fullpath, path='main.record.data.pfda.file_path')
        #self.setInClientData(value=file_url, path='main.record.data.pfda.file_url')
        self.clientPublish('floating_message', message='Upload completed')

    @public_method
    def setdata(self, file_path=None, **kwargs):
        self.fullpath = '/home/tommaso/sviluppo/genropy_projects/shipsteps/instances/shipsteps/site/files/general information ortona port.pdf'    
        self.setInClientData(value=self.fullpath, path='main.record.data.pfda.file_path')
        
