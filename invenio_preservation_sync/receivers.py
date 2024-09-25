# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Receiver for managing Preservation Sync events integration."""

from flask import g
from invenio_webhooks.models import Receiver
from marshmallow import ValidationError

from .errors import (
    InvalidStatusError,
    PermissionDeniedError,
    PreservationAlreadyReceivedError,
)
from .proxies import current_preservation_sync_service as service


class PreservationSyncReceiver(Receiver):
    """Handle incoming notification from an external preservation platform."""

    def run(self, event):
        """Process an event."""
        try:
            service.create_or_update(
                identity=g.identity,
                data=event.payload,
                event_id=event.id,
            )
        except PreservationAlreadyReceivedError as e:
            event.response_code = 409
            event.response = dict(message=str(e), status=409)
        except PermissionDeniedError as e:
            event.response_code = 403
            event.response = dict(message=str(e), status=403)
        except (InvalidStatusError, ValidationError, Exception) as e:
            event.response_code = 400
            event.response = dict(message=str(e), status=400)
