#!/usr/bin/python3
# -*- coding: utf-8 -*-

def config(root,application=None):
    pfda = root.branch('proforma da')
    pfda.thpage('clienti',table='pfda.cliente', formResource='FormCliente')
    pfda.thpage('imbarcazione',table='pfda.imbarcazione')
    pfda.thpage('proforma',table='pfda.proforma', viewResource='ViewProforma')
    pfda.thpage('Tariffe servizi portuali',table='pfda.tariffeportuali')
    pfda.thpage('tariffe',table='pfda.tariffe')
    pfda.thpage('tariffe_tipo',table='pfda.tariffa_tipo')
    pfda.thpage('ormeggiatori',table='pfda.ormeggiatori')
    pfda.thpage('agency',table='pfda.agency')
    pfda.thpage('servizi',table='pfda.servizi')
    pfda.thpage('tug',table='pfda.tug')
    pfda.thpage('pilota',table='pfda.pilota')
    pfda.thpage('serviziextra',table='pfda.serviziextra')
    pfda.thpage('customs',table='pfda.customs')
    pfda.thpage('Adm Charge',table='pfda.admcharge')
    pfda.thpage('Antifire',table='pfda.antifire')
    pfda.lookups(u"Tabelle Ausiliarie", lookup_manager="pfda")
   
