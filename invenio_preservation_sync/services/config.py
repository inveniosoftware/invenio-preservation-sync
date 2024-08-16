# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configs for the service layer to process the Preservation Sync requests."""


def can_read_permission(identity, pid):
    """Define read permission for a record's preservation information."""
    pass


def can_write_permission(identity, pid):
    """Define write permission for a record's preservation information."""
    pass


class PermissionPolicy:
    """Class to define read and write permissions for preservation information."""

    can_read = can_read_permission
    can_write = can_write_permission


PRESERVATION_SYNC_PERMISSION_POLICY = PermissionPolicy
"""Override the default permission policy to read and write preservation information."""
