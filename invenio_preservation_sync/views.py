# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Preservation Sync blueprint for Invenio platform."""


def create_preservation_info_api_bp(app):
    """Create the preservation info resource api blueprint."""
    ext = app.extensions["invenio-preservation-sync"]
    return ext.preservation_info_resource.as_blueprint()
