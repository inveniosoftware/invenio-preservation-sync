# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Service layer to process the Preservation Sync requests."""


from flask import current_app, g
from invenio_records_resources.services.uow import unit_of_work

from invenio_preservation_sync.api import PreservationInfoAPI
from invenio_preservation_sync.errors import PermissionDeniedError
from invenio_preservation_sync.services.permissions import (
    DefaultPreservationInfoPermissionPolicy,
)


class PreservationInfoResult(object):
    """Single PreservationInfo result."""

    def __init__(self, preservation):
        """Instantiate result item."""
        self.revision_id = preservation.revision_id
        self.status = preservation.status
        self.archive_timestamp = preservation.archive_timestamp
        self.harvest_timestamp = preservation.harvest_timestamp
        self.uri = preservation.uri
        self.path = preservation.path
        self.description = preservation.description

    def to_json(self):
        """Convert the result item to JSON."""
        return dict(
            revision_id=self.revision_id,
            status=self.status,
            archive_timestamp=self.archive_timestamp,
            harvest_timestamp=self.harvest_timestamp,
            uri=self.uri,
            path=self.path,
            description=dict(self.description),
        )


class PreservationInfoService(object):
    """Invenio Preservation Sync service."""

    @property
    def result_cls(self):
        """Result item class."""
        return PreservationInfoResult

    def result_item(self, preservation):
        """Return a result item."""
        if isinstance(preservation, list):
            return list(map(self.result_cls, preservation))
        return self.result_cls(preservation)

    @property
    def permission_policy(self):
        """Returns the permission policy class."""
        permission_policy_class = current_app.config.get(
            "PRESERVATION_SYNC_PERMISSION_POLICY",
            DefaultPreservationInfoPermissionPolicy,
        )
        return permission_policy_class()

    def require_permission(self, identity, action_name, record):
        """Require a specific permission from the permission policy."""
        if not self.permission_policy.check_permission(identity, action_name, record):
            raise PermissionDeniedError(action_name)

    @property
    def pid_resolver(self):
        """Return the pid resolver function."""
        return current_app.config.get(
            "PRESERVATION_SYNC_PID_RESOLVER",
        )

    @unit_of_work()
    def preserve(
        self,
        pid_id,
        revision_id,
        status,
        archive_timestamp=None,
        harvest_timestamp=None,
        uri=None,
        path=None,
        description=None,
        event_id=None,
        uow=None,
    ):
        """Process the preservation event info."""
        record = self.pid_resolver(pid_id)

        self.require_permission(g.identity, "can_write", record)

        archive_timestamp = archive_timestamp

        existing_preservation = PreservationInfoAPI.get_existing_preservation(
            record_id=record.id,
            revision_id=revision_id,
            archive_timestamp=archive_timestamp,
        )

        if existing_preservation:
            PreservationInfoAPI.update_existing_preservation(
                preservation=existing_preservation,
                status=status,
                harvest_timestamp=harvest_timestamp,
                uri=uri,
                path=path,
                description=description,
                event_id=event_id,
            )
        else:
            PreservationInfoAPI.create(
                record_id=record.id,
                revision_id=revision_id,
                status=status,
                harvest_timestamp=harvest_timestamp,
                archive_timestamp=archive_timestamp,
                uri=uri,
                path=path,
                event_id=event_id,
                description=description,
            )

    @unit_of_work()
    def get_by_record_id(self, pid_id=None, latest=False, uow=None):
        """Returns preservation info based on the record id."""
        record = self.pid_resolver(pid_id)

        self.require_permission(g.identity, "can_read", record)

        preservation = PreservationInfoAPI.get_by_record_id(record.id, latest=latest)
        if preservation:
            return self.result_item(preservation)
        else:
            return None
