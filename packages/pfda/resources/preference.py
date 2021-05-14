# preference.py
class AppPref(object):
    def prefpane_pfda(self,parent,**kwargs):
        pane = parent.contentPane(**kwargs)
        fb = pane.formbuilder()
        # Nei **kwargs c'è già il livello di path dati corretto
        fb.numbertextbox('^.garbage_df', lbl='costo standard garbage',format='#,###.00') 
        fb.numbertextbox('^.retaingarbage_df', lbl='costo standard deroga garbage',format='#,###.00')
        fb.numbertextbox('^.isps_df', lbl='costo standard isps',format='#,###.00')
        fb.numbertextbox('^.misc_df', lbl='costo standard miscellaneous',format='#,###.00')
        fb.textbox('^.notemisc_df', lbl='note standard miscellaneous', width='20em')
        fb.numbertextbox('^.bulkauth_df', lbl='costo standard aut. rinfusa',format='#,###.00')
