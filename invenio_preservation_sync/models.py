# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Models for Preservation Sync integration."""

import uuid
from enum import Enum

from invenio_db import db
from invenio_i18n import lazy_gettext as _
from invenio_webhooks.models import Event
from sqlalchemy.dialects import mysql, postgresql
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import ChoiceType, JSONType, UUIDType

PRESERVATION_STATUS_TITLES = {
    "PRESERVED": _("Preserved"),
    "PROCESSING": _("Processing"),
    "FAILED": _("Failed"),
    "DELETED": _("Deleted"),
}

PRESERVATION_STATUS_ICON = {
    "PRESERVED": "check icon",
    "PROCESSING": "spinner loading icon",
    "FAILED": "times icon",
    "DELETED": "times icon",
}

PRESERVATION_STATUS_COLOR = {
    "PRESERVED": "positive",
    "PROCESSING": "warning",
    "FAILED": "negative",
    "DELETED": "negative",
}


class PreservationStatus(str, Enum):
    """Constants for possible status of a preservation."""

    __order__ = "PRESERVED PROCESSING FAILED DELETED"

    PRESERVED = "P"
    """Release was successfully processed and published."""

    PROCESSING = "I"
    """Release is still being processed."""

    FAILED = "F"
    """Release processing has failed."""

    DELETED = "D"
    """Release has been deleted."""

    def __init__(self, value):
        """Hack."""

    def __eq__(self, other):
        """Equality test."""
        return self.value == other

    def __str__(self):
        """Return its value."""
        return self.value

    @property
    def title(self):
        """Return human readable title."""
        return PRESERVATION_STATUS_TITLES[self.name]

    @property
    def icon(self):
        """Font Awesome status icon."""
        return PRESERVATION_STATUS_ICON[self.name]

    @property
    def color(self):
        """UI status color."""
        return PRESERVATION_STATUS_COLOR[self.name]


class PreservationInfo(db.Model, Timestamp):
    """Information about the preservation."""

    __tablename__ = "preservation_info"

    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )
    """Preservation Info identifier."""

    record_id = db.Column(
        UUIDType,
        index=True,
        nullable=False,
        unique=False,
    )
    """Weak reference to a record identifier."""

    revision_id = db.Column(
        db.Integer,
        index=True,
        nullable=False,
        unique=False,
    )

    status = db.Column(
        ChoiceType(PreservationStatus, impl=db.CHAR(1)),
        nullable=False,
    )
    """Status of the preservation, e.g. 'preserved', 'processing', 'failed', etc."""

    harvest_timestamp = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        unique=False,
        index=False,
        nullable=True,
    )
    """Timestamp when the record's data was harvested."""

    archive_timestamp = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        unique=False,
        index=True,
        nullable=True,
    )
    """Timestamp when the record was archived."""

    uri = db.Column(db.String(255), unique=False, index=False, nullable=True)
    """URI to the preserved record."""

    path = db.Column(db.String(255), unique=False, index=False, nullable=True)
    """Path to the preserved record."""

    event_id = db.Column(UUIDType, db.ForeignKey(Event.id), nullable=True)
    """Incoming webhook event identifier."""

    description = db.Column(
        db.JSON()
        .with_variant(
            postgresql.JSONB(none_as_null=True),
            "postgresql",
        )
        .with_variant(
            JSONType(),
            "sqlite",
        )
        .with_variant(
            JSONType(),
            "mysql",
        ),
        default=lambda: dict(),
        nullable=True,
    )
    """Additional details in JSON format"""

    event = db.relationship(Event)
