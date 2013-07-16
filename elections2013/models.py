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
    TYPE_CENTER = 'Centre'
    TYPE_BUREAU = 'Bureau'

    TYPES = {
        TYPE_REGION: "Région",
        TYPE_CERCLE: "Cercle",
        TYPE_ARRONDISSEMENT: "Arrondissement",
        TYPE_COMMUNE: "Commune",
        TYPE_VILLAGE: "Village",
        TYPE_CENTER: 'Centre',
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
            return "{name}/{parent}".format(name=self.display_name(),
                                            parent=self.parent.display_name())
        return self.display_name()

    def parent_level(self):
        if self.parent:
            return self.parent.type
        return self.parent


class Candidate(models.Model):

    slug = models.CharField(max_length=20, primary_key=True, verbose_name=("Code"))
    last_name = models.CharField(max_length=100, verbose_name=("Nom"))
    first_name = models.CharField(max_length=100, verbose_name=("Prénom"))
    initials = models.CharField(max_length=100, verbose_name=("Initiales"))
    party = models.CharField(max_length=100, verbose_name=("Parti politique"))

    def __unicode__(self):
        return "{slug} {last_name} " \
               "{first_name} {initial}".format(slug=self.slug,
                                               last_name=self.last_name,
                                               first_name=self.first_name,
                                               initial=self.initials)


class Organization(models.Model):

    slug = models.CharField(max_length=20, primary_key=True, verbose_name=("Code"))
    name = models.CharField(max_length=100, verbose_name=("Nom"))

    def __unicode__(self):
        return "{name} {slug}".format(name=self.name, slug=self.slug)


class Reporter(models.Model):

    phone_number = models.CharField(max_length=30, null=True, blank=True,
                                    verbose_name=("Numéro de téléphone"))
    organization = models.ForeignKey('Organization', verbose_name=("Organisations"))
    voting_bureau = models.ForeignKey('Entity', verbose_name=("Bureau de vote"))
    name = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "{phone_number} {organization} " \
               "{voting_bureau}".format(phone_number=self.phone_number,
                                        organization=self.organization,
                                        voting_bureau=self.voting_bureau)


class Report(models.Model):

    class Meta:
        get_latest_by = "created_on"

    created_on = models.DateTimeField(auto_now_add=True, verbose_name=("Date de création"))
    reporter = models.ForeignKey('Reporter', verbose_name=("Rapporteur"))
    number_voters = models.PositiveIntegerField(verbose_name=("Nombre de votants"))
    number_registered = models.PositiveIntegerField(verbose_name=("Nombre d'inscrit"))
    number_spoilt = models.PositiveIntegerField(verbose_name=("Nombre de nul"))

    def __unicode__(self):
        return "{created_on} {reporter}".format(created_on=self.created_on,
                                                reporter=self.reporter)


class VoteResult(models.Model):

    report = models.ForeignKey('Report', verbose_name='Rapports')
    candidate = models.ForeignKey('Candidate', related_name='Candidats')
    votes = models.PositiveIntegerField(verbose_name=("Nombre de voix obtenues"))

    def __unicode__(self):
        return "{votes} {candidate}".format(votes=self.votes,
                                            candidate=self.candidate)
