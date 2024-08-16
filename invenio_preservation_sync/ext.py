# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module that adds Preservation Sync integration to the platform."""

from invenio_preservation_sync.services.service import PreservationInfoService

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
        if self.is_enabled(app) and self.is_configured(app):
            self.init_service(app)
            app.extensions["invenio-preservation-sync"] = self

    def init_service(self, app):
        """Initialize the service."""
        self.service = PreservationInfoService()

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("PRESERVATION_SYNC_"):
                app.config.setdefault(k, getattr(config, k))

    def is_enabled(self, app):
        """Return whether the extension is enabled."""
        return app.config.get("PRESERVATION_SYNC_INTEGRATION_ENABLED", False)

    def is_configured(self, app):
        """Return whether the extension is properly configured."""
        return bool(
            app.config.get("PRESERVATION_SYNC_PID_RESOLVER")
            and app.config.get("PRESERVATION_SYNC_GET_LIST_PATH")
            and app.config.get("PRESERVATION_SYNC_GET_LATEST_PATH")
            and app.config.get("PRESERVATION_SYNC_PERMISSION_POLICY")
        )


def finalize_app(app):
    """Finalize app."""
    pass
