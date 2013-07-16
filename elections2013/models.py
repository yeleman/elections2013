#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class Entity(MPTTModel):

    TYPE_REGION = 'region'
    TYPE_CERCLE = 'cercle'
    TYPE_ARRONDISSEMENT = 'arrondissement'
    TYPE_COMMUNE = 'commune'
    TYPE_VILLAGE = 'village'
    TYPE_CENTRE = 'Centre'
    TYPE_BUREAU = 'Bureau'

    TYPES = {
        TYPE_REGION: "Région",
        TYPE_CERCLE: "Cercle",
        TYPE_ARRONDISSEMENT: "Arrondissement",
        TYPE_COMMUNE: "Commune",
        TYPE_VILLAGE: "Village",
        TYPE_CENTRE: 'Centre',
        TYPE_BUREAU: 'Bureau'
    }

    slug = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=TYPES.items())
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children',
                            verbose_name="Parent")

    objects = TreeManager()

    def __unicode__(self):
        return self.name

    def display_name(self):
        return self.name.title()

    def display_full_name(self):
        if self.parent:
            return "%(name)s/%(parent)s" % {'name': self.display_name(),
                                            'parent': self.parent.display_name()}
        return self.display_name()

    def parent_level(self):
        if self.parent:
            return self.parent.type
        return self.parent


class Candidate(models.Model):
    """ Les candidat de l'election pour l'election """

    class Meta:
        get_latest_by = "last_name"

    slug = models.CharField(max_length=20, primary_key=True, verbose_name=("Code"))
    last_name = models.CharField(max_length=100, verbose_name=("Nom"))
    first_name = models.CharField(max_length=100, verbose_name=("Prénom"))
    initial = models.CharField(max_length=100, verbose_name=("Initial"))
    party = models.CharField(max_length=100, verbose_name=("Parti politiques"))

    def __unicode__(self):
        return "%(slug)s %(last_name)s " \
               "%(first_name)s %(initial)s" % {"slug": self.slug,
                                               "last_name": self.last_name,
                                               "first_name": self.first_name,
                                               "initial": self.initial}


class Organization(models.Model):
    """ Les partis politiques """

    class Meta:
        get_latest_by = "name"

    slug = models.CharField(max_length=20, primary_key=True, verbose_name=("Code"))
    name = models.CharField(max_length=100, verbose_name=("Nom"))

    def __unicode__(self):
        return "%(name)s %(slug)s" % {"name": self.name, "slug": self.slug}


class Reporter(models.Model):
    """ Les Rapporteurs des partis politiques """

    class Meta:
        get_latest_by = "phone_number"

    phone_number = models.CharField(max_length=30, verbose_name=("Numéro de téléphone"))
    organization = models.ForeignKey('Organization', verbose_name=("Organisations"))
    pollcenter = models.ForeignKey('Entity', verbose_name=("Bureau de vote"))

    def __unicode__(self):
        return "%(phone_number)s %(organization)s %(pollcenter)s" % {"phone_number": self.phone_number,
                                                                     "organization": self.organization,
                                                                     "pollcenter": self.pollcenter}


class Report(models.Model):
    """ Le rapport envoyé par les assesseurs depuis le bureaux de votes"""

    class Meta:
        get_latest_by = "created_on"

    created_on = models.DateTimeField(auto_now_add=True, verbose_name=("Date de création"))
    reporter = models.ForeignKey('Reporter', verbose_name=("Rapporteur"))
    number_voters = models.PositiveIntegerField(verbose_name=("Nombre de votants"))
    number_registered = models.PositiveIntegerField(verbose_name=("Nombre d'inscrit"))
    spoiled_ballot = models.PositiveIntegerField(verbose_name=("Bulletin nul"))

    def __unicode__(self):
        return "%(created_on)s %(reporter)s" % {"created_on": self.created_on,
                                                "reporter": self.reporter}


class Vote(models.Model):
    """ le resultat de chanque candidat """

    class Meta:
        get_latest_by = "votes_obtained"

    report = models.ForeignKey('Report', verbose_name='Rapports')
    candidate = models.ForeignKey('Candidate', related_name='Candidats')
    votes_obtained = models.PositiveIntegerField(verbose_name=("Nombre de voix obtenu"))

    def __unicode__(self):
        return "%(votes_obtained)s %(candidate)s" % {"votes_obtained": self.votes_obtained,
                                                     "candidate": self.candidate}
