# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for the service layer to process the Preservation Sync requests."""


class DefaultPreservationInfoPermissionPolicy(object):
    """Default permission policy to read and write the PreservationInfo."""

    def can_read(self, identity, record):
        """Return if identity has permission to read the given record's preservation info."""
        raise NotImplementedError()

    def can_write(self, identity, record):
        """Return if identity has permission to write the given record's preservation info."""
        raise NotImplementedError()

    def check_permission(self, identity, action_name, record):
        """Return if identity has permission to execute the action on the given record."""
        try:
            has_permission = getattr(self, action_name)
        except AttributeError:
            return False
        return has_permission(identity, record)
