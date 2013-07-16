#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib import admin

from elections2013.models import (Entity, Candidate, Organization,
                                  Reporter, Report, VoteResult)


class CustomCandidate(admin.ModelAdmin):
    list_display = ("slug", "initials", "first_name", "last_name", "party")
    list_filter = ("party",)


class CustomOrganization(admin.ModelAdmin):
    list_display = ("slug", "name")
    list_filter = ("name",)


class CustomEntity(admin.ModelAdmin):
    list_display = ("slug", "name", "type", "latitude",
                    "longitude", "parent",)


class CustomReporter(admin.ModelAdmin):
    list_display = ("phone_number", "organization", "voting_bureau", "name")
    list_filter = ("organization",)


class ModelInline(admin.StackedInline):
    model = VoteResult
    extra = 0


class CustomReport(admin.ModelAdmin):
    list_display = ("created_on", "reporter", "number_registered",
                    "number_voters", "number_spoilt")
    # list_filter = ("result",)
    inlines = [ModelInline]


class CustomVoteResult(admin.ModelAdmin):
    list_display = ("votes", "candidate")
    list_filter = ("report__reporter__organization",)

admin.site.register(Candidate, CustomCandidate)
admin.site.register(Organization, CustomOrganization)
admin.site.register(Entity, CustomEntity)
admin.site.register(Report, CustomReport)
admin.site.register(Reporter, CustomReporter)
admin.site.register(VoteResult, CustomVoteResult)
