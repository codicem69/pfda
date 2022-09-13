#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('description')
        r.fieldcell('pathfile')

    def th_order(self):
        return 'description'

    def th_query(self):
        return dict(column='description', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('description')
        fb.field('pathfile', width='60em', readOnly=True)
        fb.br()            
        fb.div("Documento port info da allegare all'email", height='0px', padding='20px')  
        fb.br()          
        fb.div(hidden='^.pathfile?=#v', lbl='File').dropUploader(height='100px', width='320px',colspan=2,
                            label="<div style='padding:5px'>Drop document port general info here <br>or double click</div>",
                            uploadPath='site:files', 
                            progressBar=True,
                            onUploadedMethod=self.uploadFile)
        fb.button('!![en]Remove file', hidden='^.pathfile?=!#v').dataRpc(self.deleteFile, file='=.pathfile', record='=#FORM.record', _onResult="this.form.reload();")

    @public_method
    def uploadFile(self, file_path=None, **kwargs):
        fileSn = self.site.storageNode(file_path)
        fullpath = fileSn.internal_path
        self.setInClientData(value=fullpath, path='pfda_fileforemail.form.record.pathfile')
        self.clientPublish('floating_message', message='Upload completed')

    @public_method
    def deleteFile(self, file=None, record=None,**kwargs):
        #os.remove(file)
        pkeys=record['id']
        self.db.table('pfda.fileforemail').deleteSelection(where='$id =:pkeys', pkeys=pkeys)
        self.db.commit()
       # self.setInClientData(value=None, path='pfda_fileforemail.form.record.pathfile')
        #self.setInClientData(value=None, path='pfda_fileforemail.form.record.description')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
