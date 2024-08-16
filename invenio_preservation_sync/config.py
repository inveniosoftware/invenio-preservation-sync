# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configuration for Preservation Sync module."""

PRESERVATION_SYNC_INTEGRATION_ENABLED = False
"""Enables the preservation sync integration."""

PRESERVATION_SYNC_GET_LIST_PATH = "/records/<id>/preservations"
"""API path to get the all preservation statuses."""

PRESERVATION_SYNC_GET_LATEST_PATH = "/records/<id>/preservations/latest"
"""API path to get the latest preservation status."""


def resolve_record_pid(pid):
    """Default function to resolve the pid to the record object."""
    return None


PRESERVATION_SYNC_PID_RESOLVER = resolve_record_pid
"""Function to resolve the pid to the record object."""
