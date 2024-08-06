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


class InvalidSenderError(PreservationSyncError):
    """Invalid preservation info sender error."""

    message = "Invalid sender for event."

    def __init__(self, event=None, user=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.event = event
        self.user = user


class PreservationAlreadyReceivedError(PreservationSyncError):
    """Same preservation info already received error."""

    message = "The preservation info has already been received."

    def __init__(self, preservation=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.preservation = preservation


class MissingConfigError(PreservationSyncError):
    """Mandatory configuration missing to use the module."""

    message = "Mandatory configuration missing for the module."

    def __init__(self, config=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.config = config
