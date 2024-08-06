# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Receiver for managing Preservation Sync events integration."""

from flask import current_app, g
from invenio_webhooks.models import Receiver
from werkzeug.exceptions import BadRequest

from invenio_preservation_sync.api import PreservationInfoAPI
from invenio_preservation_sync.utils import get_mandatory_config

from .errors import (
    InvalidSenderError,
    MissingConfigError,
    PreservationAlreadyReceivedError,
)


class PreservationSyncReceiver(Receiver):
    """Handle incoming notification from GitHub on a new release."""

    def run(self, event):
        """Process an event."""
        try:
            perm_policy = get_mandatory_config(
                current_app, "PRESERVATION_SYNC_PERMISSION_POLICY"
            )
            pid_resolver = get_mandatory_config(
                current_app, "PRESERVATION_SYNC_PID_RESOLVER"
            )

            pid_id = event.payload.get("pid")
            revision_id = event.payload.get("revision_id")
            status = event.payload.get("status")

            if not pid_id or not revision_id or not status:
                raise BadRequest("Mandatory fields are missing from the request.")

            record_uuid = pid_resolver(pid_id)

            if not perm_policy.can_write(g.identity, record_uuid):
                raise InvalidSenderError(event, g.identity)

            archive_timestamp = event.payload.get("archive_timestamp")

            existing_preservation = PreservationInfoAPI.get_existing_preservation(
                record_id=record_uuid,
                revision_id=revision_id,
                archive_timestamp=archive_timestamp,
            )

            if existing_preservation:
                PreservationInfoAPI.update_existing_preservation(
                    preservation=existing_preservation,
                    status=status,
                    harvest_timestamp=event.payload.get("harvest_timestamp"),
                    uri=event.payload.get("uri"),
                    path=event.payload.get("path"),
                    description=event.payload.get("description"),
                    event=event,
                )
            else:
                # Create the Preservation
                PreservationInfoAPI.create(
                    record_id=record_uuid,
                    revision_id=revision_id,
                    status=status,
                    harvest_timestamp=event.payload.get("harvest_timestamp"),
                    archive_timestamp=archive_timestamp,
                    uri=event.payload.get("uri"),
                    path=event.payload.get("path"),
                    event=event,
                    description=event.payload.get("description"),
                )
        except PreservationAlreadyReceivedError as e:
            event.response_code = 409
            event.response = dict(message=str(e), status=409)
        except InvalidSenderError as e:
            event.response_code = 403
            event.response = dict(message=str(e), status=403)
        except (MissingConfigError, BadRequest, ValueError) as e:
            event.response_code = 400
            event.response = dict(message=str(e), status=400)
