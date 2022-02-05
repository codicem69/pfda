#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tipo')
        r.fieldcell('nome',width='20em')
        r.fieldcell('bandiera')
        r.fieldcell('loa')
        r.fieldcell('gt')
        r.fieldcell('nt')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('tipo' )
        fb.field('nome' )
        fb.field('bandiera' )
        fb.field('loa' )
        fb.field('gt' )
        fb.field('nt' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
