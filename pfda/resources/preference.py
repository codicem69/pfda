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
        fb.textbox('^.notemisc_df', lbl='note standard miscellaneous', width='60em')
        fb.numbertextbox('^.bulkauth_df', lbl='costo standard aut. rinfusa',format='#,###.00')
        fb.simpleTextArea('^.notestandard',lbl='Note Standard',width='60em', height='200px',editor=True)
        fb.dbSelect(value='^.mail.account_id', lbl='Mail account', table='email.account',columns='$',auxColumns='$full_name', hasDownArrow=True)
        fb.dbSelect(value='^.tpl.template_id', lbl='Template',
                        table='adm.userobject', hasDownArrow=True, condition='$objtype=:tpl', condition_tpl='template',
                        rowcaption='$code,$description', auxColumns='$description,$userid', selected_tbl='^.tpl.tbl')
        fb.img(src='^.timbro',lbl='Timbro',
                    border='2px dotted silver',
                    crop_width='150px',
                    crop_height='150px',
                    edit=True,
                    placeholder=True,
                    upload_filename='timbro_societa',
                    upload_folder='site:timbro/image')
