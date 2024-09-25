# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configuration for Preservation Sync module."""

PRESERVATION_SYNC_ENABLED = False
"""Enables the preservation sync integration."""

PRESERVATION_SYNC_GET_LIST_PATH = "/records/<pid_id>/preservations"
"""API path to get the all preservation statuses."""

PRESERVATION_SYNC_GET_LATEST_PATH = "/records/<pid_id>/preservations/latest"
"""API path to get the latest preservation status."""

PRESERVATION_SYNC_PID_RESOLVER = None
"""Function to resolve the pid to the object uuid."""

PRESERVATION_SYNC_PERMISSION_POLICY = None
"""Override the default permission policy to read and write preservation information."""
