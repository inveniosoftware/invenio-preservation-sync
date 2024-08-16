# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Preservation Sync API abstraction for the PreservationInfo entity."""

from dateutil.parser import parse
from invenio_db import db
from sqlalchemy.sql import text

from invenio_preservation_sync.errors import PreservationAlreadyReceivedError
from invenio_preservation_sync.models import PreservationInfo, PreservationStatus


class PreservationInfoAPI(object):
    """
    API abstraction of a PreservationInfo entity.

    This class provides an abstraction layer for interacting with PreservationInfo objects.
    It encapsulates the functionality for creating, retrieving, and managing them.
    """

    @classmethod
    def create(
        cls,
        record_id,
        revision_id,
        status,
        harvest_timestamp=None,
        archive_timestamp=None,
        uri=None,
        path=None,
        event_id=None,
        description=None,
    ):
        """Create a Preservation Information."""
        status = PreservationInfoAPI._convert_status(status)
        preservation = PreservationInfo(
            record_id=record_id,
            revision_id=revision_id,
            status=status,
            harvest_timestamp=harvest_timestamp,
            archive_timestamp=archive_timestamp,
            uri=uri,
            path=path,
            event_id=event_id,
            description=description,
        )

        db.session.add(preservation)
        db.session.commit()
        return preservation

    @classmethod
    def get_by_record_id(cls, record_id=None, latest=False):
        """Get Preservation Info by record id."""
        preservation = PreservationInfo.query.filter_by(record_id=record_id).order_by(
            PreservationInfo.revision_id.desc(),
            PreservationInfo.archive_timestamp.desc(),
            PreservationInfo.created.desc(),
        )
        if latest:
            return preservation.first()
        return preservation.all()

    @classmethod
    def get_existing_preservation(
        cls,
        record_id=None,
        revision_id=None,
        archive_timestamp=None,
    ):
        """Return Preservation Info if it already exists."""
        preservation = PreservationInfo.query.filter_by(
            record_id=record_id,
            revision_id=revision_id,
            archive_timestamp=archive_timestamp,
        ).first()
        return preservation

    @classmethod
    def update_existing_preservation(
        cls,
        preservation,
        status=None,
        harvest_timestamp=None,
        uri=None,
        path=None,
        event_id=None,
        description=None,
    ):
        """Update existing preservation."""
        status = PreservationInfoAPI._convert_status(status)

        if (
            preservation.status == status
            and preservation.harvest_timestamp == parse(harvest_timestamp)
            and preservation.uri == uri
            and preservation.path == path
            and preservation.description == description
        ):
            raise PreservationAlreadyReceivedError(preservation)

        if status:
            preservation.status = status

        if harvest_timestamp:
            preservation.harvest_timestamp = harvest_timestamp

        if uri:
            preservation.uri = uri

        if path:
            preservation.path = path

        if description:
            preservation.description = description

        preservation.event_id = event_id

        db.session.commit()

    @classmethod
    def _convert_status(cls, value):
        """Convert the status of the preservation info.

        Valid examples: "P", "Preserved", "preserved"
        """
        if isinstance(value, PreservationStatus):
            return value
        elif isinstance(value, str):
            upper_value = value.upper()
            if PreservationStatus.has_key(upper_value):
                return PreservationStatus[upper_value]
            return PreservationStatus(value.upper())
        else:
            raise TypeError("Value must be a PreservationStatus or a string.")
