# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Receiver for managing Preservation Sync events integration."""

from invenio_webhooks.models import Receiver
from werkzeug.exceptions import BadRequest

from invenio_preservation_sync.proxies import (
    current_preservation_sync_service as service,
)

from .errors import PermissionDeniedError, PreservationAlreadyReceivedError


class PreservationSyncReceiver(Receiver):
    """Handle incoming notification from an external preservation platform."""

    def run(self, event):
        """Process an event."""
        try:
            pid_id = event.payload.get("pid")
            revision_id = event.payload.get("revision_id")
            status = event.payload.get("status")

            if not pid_id or not revision_id or not status:
                raise BadRequest("Mandatory fields are missing from the request.")

            service.preserve(
                pid_id,
                revision_id,
                status,
                archive_timestamp=event.payload.get("archive_timestamp"),
                harvest_timestamp=event.payload.get("harvest_timestamp"),
                uri=event.payload.get("uri"),
                path=event.payload.get("path"),
                description=event.payload.get("description"),
                event_id=event.id,
            )
        except PreservationAlreadyReceivedError as e:
            event.response_code = 409
            event.response = dict(message=str(e), status=409)
        except PermissionDeniedError as e:
            event.response_code = 403
            event.response = dict(message=str(e), status=403)
        except (BadRequest, TypeError, Exception) as e:
            event.response_code = 400
            event.response = dict(message=str(e), status=400)
