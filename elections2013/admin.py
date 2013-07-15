#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin

from elections2013.models import (Entity, Candidate, Organization,
                                  Reporter, Report, Vote)


class CustomCandidate(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "party")
    list_filter = ("last_name", "first_name", "party")


class CustomOrganization(admin.ModelAdmin):
    list_display = ("slug", "name")
    list_filter = ("name",)


class CustomEntity(admin.ModelAdmin):
    list_display = ("slug", "name", "type", "latitude",
                    "longitude", "parent",)


class CustomReporter(admin.ModelAdmin):
    list_display = ("phone_number", "party",)
    list_filter = ("phone_number", "party")


class ModelInline(admin.StackedInline):
    model = Vote
    extra = 0


class CustomReport(admin.ModelAdmin):
    list_display = ("created_on", "reporter", "number_voters",
                    "number_registered", "spoiled_ballot")
    # list_filter = ("result",)
    inlines = [ModelInline]


class CustomVote(admin.ModelAdmin):
    list_display = ("votes_obtained", "candidate")
    list_filter = ("votes_obtained",)

admin.site.register(Candidate, CustomCandidate)
admin.site.register(Organization, CustomOrganization)
admin.site.register(Entity, CustomEntity)
admin.site.register(Report, CustomReport)
admin.site.register(Reporter, CustomReporter)
admin.site.register(Vote, CustomVote)
