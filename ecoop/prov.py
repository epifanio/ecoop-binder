# /usr/bin/env python
# -*- coding: utf-8 -*-

# ##############################################################################
#
#
# Project: ECOOP, sponsored by The National Science Foundation
# Purpose: this code is part of the Cyberinfrastructure developed for the ECOOP project
# http://tw.rpi.edu/web/project/ECOOP
#                from the TWC - Tetherless World Constellation
#                            at RPI - Rensselaer Polytechnic Institute
#                            founded by NSF
#
# Author:   Massimo Di Stefano , distem@rpi.edu -
#                http://tw.rpi.edu/web/person/MassimoDiStefano
#
###############################################################################
# Copyright (c) 2008-2014 Tetherless World Constellation at Rensselaer Polytechnic Institute
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

def initProv():
    prov = {"@id": "http://not.sure/yet#notebook_run",
        "@type": [
            "http://www.w3.org/ns/prov#Activity"
        ]}
    return prov

def provStartedAtTime(now):
    StartedAtTime = [{"@type": "http://www.w3.org/2001/XMLSchema#dateTime",
                      "@value": '%s' % now
                      }]
    return StartedAtTime

def provEndedAtTime(now):
    EndedAtTime = [{"@type": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "@value": '%s' % now
                    }]
    return EndedAtTime

def provWasAssociatedWith(usernames):
    usernames = usernames.split(" ")
    WasAssociatedWith = []
    for i in usernames:
        user = {"@id": "http://tw.rpi.edu/instances/%s" % i}
        WasAssociatedWith.append(user)
    return WasAssociatedWith


def provUsed(software):
    software = software.split(" ")
    provUsed = []
    for i in software:
        sw = {"@id": "ex:%s" % i}
        WasAssociatedWith.append(sw)
    return provUsed


def provcontext():
    context = """"{
    _comment": "Classes and properties that are not defined in the ecoop ontology are assigned the prefix ecoop_ext. We may do one of the following things: 1) Skip collecting these pieces of information; 2) Extend the ecoop ontology to include these properties and classes; 3) Find existing properties and classes, not necessarily in the ecoop ontology, to take their places.",
    "@context": {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "ecoop": "http://escience.rpi.edu/ontology/eco-op/ecoopProv.ttl#",
        "owl": "http://www.w3.org/2002/07/owl#",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "skos": "http://www.w3.org/2009/08/skos-reference/skos.rdf#",
        "dctype": "http://purl.org/dc/dcmitype/",
        "prov": "http://www.w3.org/ns/prov#",
        "dct": "http://purl.org/dc/terms/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "dcat": "http://www.w3.org/ns/dcat#",
        "qudt": "http://qudt.org/1.1/schema/qudt#",
        "ex" : "http://not.sure/yet#",
        "ecoop_ext": "http://escience.rpi.edu/ontology/eco-op/ecoopProvExt.ttl#"
    },
    "@graph": [
        {}]
    }"""
    return context