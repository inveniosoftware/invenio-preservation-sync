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

    query_order = "revision_id desc, archive_timestamp desc, created desc"

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
        event=None,
        description=None,
    ):
        """Create a Preservation Information."""
        status = PreservationInfoAPI.convert_status(status)
        preservation = PreservationInfo(
            record_id=record_id,
            revision_id=revision_id,
            status=status,
            harvest_timestamp=harvest_timestamp,
            archive_timestamp=archive_timestamp,
            uri=uri,
            path=path,
            event=event,
            description=description,
        )

        db.session.add(preservation)
        db.session.commit()
        return preservation

    @classmethod
    def get_by_record_id(cls, record_id):
        """Get Preservation Info by record id."""
        preservations = PreservationInfo.query.filter_by(record_id=record_id).order_by(
            text(cls.query_order)
        )
        return preservations

    @classmethod
    def get_latest_by_record_id(cls, record_id):
        """Get latest Preservation Info for the given record id."""
        preservation = (
            PreservationInfo.query.filter_by(record_id=record_id)
            .order_by(text(cls.query_order))
            .first()
        )
        return preservation

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
        event=None,
        description=None,
    ):
        """Update existing preservation."""
        status = PreservationInfoAPI.convert_status(status)

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

        preservation.event = event

        db.session.commit()

    @classmethod
    def convert_status(cls, value):
        """Convert the status of the preservation info.

        Valid examples: "P", "Preserved", "preserved"
        """
        if isinstance(value, str):
            if value in [x.value for x in PreservationStatus]:
                return PreservationStatus(value)
            elif value.upper() in [x.name for x in PreservationStatus]:
                return PreservationStatus[value.upper()]
        elif isinstance(value, PreservationStatus):
            return value
        raise ValueError(
            f"Invalid status value for the Preservation Status. Got: {value}"
        )

    @classmethod
    def convert_to_dict(cls, preservation):
        """Convert the results to dict."""
        if isinstance(preservation, list):
            res = []
            for p in preservation:
                res.append({c.name: getattr(p, c.name) for c in p.__table__.columns})
            return res
        return {
            c.name: getattr(preservation, c.name)
            for c in preservation.__table__.columns
        }
