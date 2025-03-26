#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrstructures import GnrStructData, valid_children
from gnr.core.gnrbag import Bag

class ProformaStruttura(GnrStructData):
    default_childname = '*'

    @valid_children(servizi_extra='1:',pilot='1:',moor='1:',tug='1:',antifire='1:',admcharge='1:')
    def proforma(self, cliente_id=None,imbarcazione_id=None, data=None, agency_id=None,cargo=None,dangerous_cargo=None,notepilot=None,notemoor=None,
                 notetug=None,agency=None,noteagency=None,customs=None,notecustoms=None,garbage=None,notegarbage=None,retaingarbage=None,noteretaingb=None,
                 isps=None,noteisps=None,misc=None,notemisc=None,bulkauth=None,notebulk=None,totantifire=None,noteantifire=None,stamp=None,noteproforma=None):
        
        return self.child('proforma', cliente_id=cliente_id, imbarcazione_id=imbarcazione_id, data=data, agency_id=agency_id,cargo=cargo,
                          dangerous_cargo=dangerous_cargo,notepilot=notepilot,notemoor=notemoor,notetug=notetug,agency=agency,noteagency=noteagency,
                          customs=customs,notecustoms=notecustoms,garbage=garbage,notegarbage=notegarbage,retaingarbage=retaingarbage,noteretaingb=noteretaingb,
                          isps=isps,noteisps=noteisps,misc=misc,notemisc=notemisc,bulkauth=bulkauth,notebulk=notebulk,totantifire=totantifire,
                          noteantifire=noteantifire,stamp=stamp,noteproforma=noteproforma)

    @valid_children()
    def servizi_extra(self, servizi_id=None, descrizione=None, tariffa=None):
        return self.child('servizi_extra', servizi_id=servizi_id, descrizione=descrizione, tariffa=tariffa)
    
    @valid_children()
    def pilot(self, tariffe_id=None, quantita=None, ovt=None,pu=None,totpilot=None):
        return self.child('pilot', tariffe_id=tariffe_id, quantita=quantita, ovt=ovt)#, pu=pu, totpilot=totpilot)
    
    @valid_children()
    def moor(self, tariffe_id=None, quantita=None, ovt=None,pu=None,totmoor=None):
        return self.child('moor', tariffe_id=tariffe_id, quantita=quantita, ovt=ovt)#, pu=pu, totmoor=totmoor)
    
    @valid_children()
    def tug(self, tariffe_id=None, quantita=None,numero_tug=None, ovt=None,pu=None,tottug=None):
        return self.child('tug', tariffe_id=tariffe_id, quantita=quantita, numero_tug=numero_tug, ovt=ovt)#, pu=pu, tottug=tottug)
    
    @valid_children()
    def antifire(self, tariffe_id=None, quantita=None,ore=None, pu=None,totantifire=None):
        return self.child('antifire', tariffe_id=tariffe_id, quantita=quantita, ore=ore)#, pu=pu, totantifire=totantifire)
    
    @valid_children()
    def admcharge(self, tariffe_id=None, quantita=None, pu=None,totadmcharge=None):
        return self.child('admcharge', tariffe_id=tariffe_id, quantita=quantita)#, pu=pu, totadmcharge=totadmcharge)

class ProformaManager(object):
    def __init__(self, db):
        self.db = db

        self.proforma_record = GnrStructData() # Bag() ?
        self.tblproforma = self.db.table('pfda.proforma')
        self.tblserviziextra = self.db.table('pfda.serviziextra')
        self.tblpilot = self.db.table('pfda.pilota')
        self.tblmoor = self.db.table('pfda.ormeggiatori')
        self.tbltug = self.db.table('pfda.tug')
        self.tblantifire = self.db.table('pfda.antifire')
        self.tbladmcharge = self.db.table('pfda.admcharge')

    def duplicaProforma(self, proforma_id, agency_id,cargo,dangerous_cargo,notepilot,notemoor,notetug,agency,noteagency,customs,notecustoms,garbage,
                                notegarbage,retaingarbage,noteretaingb,isps,noteisps,misc,notemisc,bulkauth,notebulk,noteantifire,stamp,noteproforma):
        proforma_corrente = self.tblproforma.record(proforma_id,agency_id, mode='bag')
        
        self.proforma_record = ProformaStruttura() # creo lo scheletro del proforma in formato Struct
        pfda = self.proforma_record.proforma(cliente_id=proforma_corrente['cliente_id'],imbarcazione_id=proforma_corrente['imbarcazione_id'],agency_id=proforma_corrente['agency_id'], data=self.db.workdate,
                                             cargo=proforma_corrente['cargo'],dangerous_cargo=proforma_corrente['dangerous_cargo'],notepilot=proforma_corrente['notepilot'],
                                             notemoor=proforma_corrente['notemoor'],notetug=proforma_corrente['notetug'],agency=proforma_corrente['agency'],
                                             noteagency=proforma_corrente['noteagency'],customs=proforma_corrente['customs'],notecustoms=proforma_corrente['notecustoms'],
                                             garbage=proforma_corrente['garbage'],notegarbage=proforma_corrente['notegarbage'],retaingarbage=proforma_corrente['retaingarbage'],
                                             noteretaingb=proforma_corrente['noteretaingb'],isps=proforma_corrente['isps'],noteisps=proforma_corrente['noteisps'],misc=proforma_corrente['misc'],
                                             notemisc=proforma_corrente['notemisc'],bulkauth=proforma_corrente['bulkauth'],notebulk=proforma_corrente['notebulk'],
                                             noteantifire=proforma_corrente['noteantifire'],stamp=proforma_corrente['stamp'],noteproforma=proforma_corrente['noteproforma'])
        
        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tblserviziextra.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.servizi_extra(servizi_id=riga['servizi_id'], descrizione=riga['descrizione'],tariffa=riga['tariffa'] )
        
        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tblpilot.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.pilot(tariffe_id=riga['tariffe_id'], quantita=riga['quantita'],ovt=riga['ovt'],pu=riga['pu'],totpilot=riga['totpilot'] )
        
        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tblmoor.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.moor(tariffe_id=riga['tariffe_id'], quantita=riga['quantita'],ovt=riga['ovt'],pu=riga['pu'],totmoor=riga['totmoor'] )
        
        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tbltug.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.tug(tariffe_id=riga['tariffe_id'], quantita=riga['quantita'],numero_tug=riga['numero_tug'],ovt=riga['ovt'],pu=riga['pu'],tottug=riga['tottug'] )

        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tblantifire.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.antifire(tariffe_id=riga['tariffe_id'], quantita=riga['quantita'],ore=proforma_corrente['ore'],pu=riga['pu'],totantifire=riga['totantifire'] )

        # localizza le righe di questo proforma_corrente perché dobbiamo caricarle nella Struct
        righe_correnti = self.tbladmcharge.query(where='$proforma_id = :pfda_id', pfda_id=proforma_corrente['id']).fetch()
        for riga in righe_correnti: # nella 'struttura' del proforma inserisce le righe usando i dati delle righe originali
            pfda.admcharge(tariffe_id=riga['tariffe_id'], quantita=riga['quantita'],pu=riga['pu'],totadmcharge=riga['totadmcharge'] )

    def scriviProforma(self):
        
        #self.proforma_record.validate()
        
        self.tblproforma.insert(self.proforma_record.getAttr('proforma'))

        for riga_node in self.proforma_record['proforma']: # mmm ogni riga è un BagNode
            riga_record = riga_node.attr
            riga_record['proforma_id'] = self.proforma_record.getAttr('proforma', 'id')
            if riga_node.attr['tag']=='servizi_extra':
                self.tblserviziextra.insert(riga_record)
            if riga_node.attr['tag']=='pilot':
                self.tblpilot.insert(riga_record)
            if riga_node.attr['tag']=='moor':
                self.tblmoor.insert(riga_record)
            if riga_node.attr['tag']=='tug':
                self.tbltug.insert(riga_record)
            if riga_node.attr['tag']=='antifire':
                self.tblantifire.insert(riga_record)
            if riga_node.attr['tag']=='admcharge':
                self.tbladmcharge.insert(riga_record)
        self.db.commit()
