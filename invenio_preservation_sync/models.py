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


class PreservationStatus(str, Enum):
    """Constants for possible statuses of a preservation."""

    __order__ = "PRESERVED PROCESSING FAILED DELETED"

    PRESERVED = "P"
    """Record was successfully processed and preserved."""

    PROCESSING = "I"
    """Record is still being processed."""

    FAILED = "F"
    """Record preservation has failed."""

    DELETED = "D"
    """Record preservation has been deleted."""

    def __eq__(self, other):
        """Equality test."""
        return self.value == other

    def __str__(self):
        """Return its value."""
        return self.value

    @classmethod
    def has_key(cls, name):
        """Return if name is in keys."""
        return name in cls.__members__


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
