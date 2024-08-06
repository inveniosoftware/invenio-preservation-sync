# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module that adds Preservation Sync integration to the platform."""

from . import config


class InvenioPreservationSync(object):
    """Invenio-Preservation-Sync extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-preservation-sync"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("PRESERVATION_SYNC_"):
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize app."""
    pass
