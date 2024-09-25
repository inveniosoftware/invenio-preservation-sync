# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Preservation-Sync errors."""

import marshmallow as ma
from flask_resources import HTTPJSONException, create_error_handler


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


class MissingConfigError(PreservationSyncError):
    """Mandatory configuration missing error."""

    message = "Mandatory config is missing to enable Preservation Sync."

    def __init__(self, message=None):
        """Constructor."""
        super().__init__(message or self.message)


class PreservationInfoNotFoundError(PreservationSyncError):
    """Preservation Info not found error."""

    message = "No preservation info was found for the given PID."

    def __init__(self, message=None):
        """Constructor."""
        super().__init__(message or self.message)


class InvalidStatusError(PreservationSyncError):
    """Invalid status error."""

    message = "The given status was not valid."

    def __init__(self, status=None, message=None):
        """Constructor."""
        super().__init__(message or self.message)
        self.status = status


class ErrorHandlersMixin:
    """Mixin to define error handlers."""

    error_handlers = {
        InvalidStatusError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=e.message,
            )
        ),
        ma.ValidationError: create_error_handler(
            lambda e: HTTPJSONException(
                code=400,
                description=e.message,
            )
        ),
        PermissionDeniedError: create_error_handler(
            lambda e: HTTPJSONException(
                code=403,
                description=e.message,
            )
        ),
        PreservationInfoNotFoundError: create_error_handler(
            lambda e: HTTPJSONException(
                code=404,
                description=e.message,
            )
        ),
    }
