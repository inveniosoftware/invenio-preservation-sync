# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Preservation-Sync errors."""


class PreservationSyncError(Exception):
    """General Preservation-Sync error."""


class PermissionDeniedError(PreservationSyncError):
    """Not authorized to read preservation info."""

    message = "User does not have permission for the requested action."

    def __init__(self, action_name=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.action_name = action_name


class PreservationAlreadyReceivedError(PreservationSyncError):
    """Same preservation info already received error."""

    message = "The preservation info has already been received."

    def __init__(self, preservation=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.preservation = preservation
