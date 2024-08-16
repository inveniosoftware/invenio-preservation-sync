# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import uuid

import mock
import pytest
from flask_principal import AnonymousIdentity, RoleNeed
from invenio_accounts.models import Role
from invenio_app.factory import create_api as _create_api
from invenio_oauth2server.models import Token

from invenio_preservation_sync.services.permissions import (
    DefaultPreservationInfoPermissionPolicy,
)


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config override."""
    app_config["PRESERVATION_SYNC_INTEGRATION_ENABLED"] = True
    app_config["PRESERVATION_SYNC_PID_RESOLVER"] = test_resolve_record_pid
    app_config["PRESERVATION_SYNC_GET_LIST_PATH"] = "/records/<id>/preservations"
    app_config["PRESERVATION_SYNC_GET_LATEST_PATH"] = (
        "/records/<id>/preservations/latest"
    )
    app_config["PRESERVATION_SYNC_PERMISSION_POLICY"] = PermissionPolicy
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_api


@pytest.fixture(scope="session", autouse=True)
def generate_uuids():
    """Random generate uuids as global vars."""
    global PUBLIC_UUID
    PUBLIC_UUID = uuid.uuid4()

    global RESTRICTED_UUID
    RESTRICTED_UUID = uuid.uuid4()


def test_resolve_record_pid(pid):
    """PID resolver."""
    record = mock.Mock()
    if pid == "public_pid":
        record.id = PUBLIC_UUID
        record.access = "public"
        return record
    elif pid == "restricted_pid":
        record.id = RESTRICTED_UUID
        record.access = "restricted"
        return record
    raise Exception("PID does not exists.")


def can_read_permission(self, identity, record):
    """Can read permission."""
    if record.access == "public" or (
        not isinstance(identity, AnonymousIdentity)
        and "archiver" in identity.user.roles
    ):
        return True
    return False


def can_write_permission(self, identity, record):
    """Can write permission."""
    if "archiver" in identity.user.roles:
        return True
    return False


class PermissionPolicy(DefaultPreservationInfoPermissionPolicy):  # noqa: D400
    """Permission Policy."""

    can_read = can_read_permission
    can_write = can_write_permission


@pytest.fixture()
def archiver_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed."""
    role = Role(name="archiver")
    db.session.add(role)
    db.session.commit()
    return RoleNeed("archiver")


@pytest.fixture()
def archiver(UserFixture, app, db, archiver_role_need):
    """Archiver user for requests."""
    u = UserFixture(
        email="archiver@inveniosoftware.org",
        password="archiver",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "archiver")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u


@pytest.fixture()
def access_token(app, db, archiver):
    """Fixture that create an access token."""
    token = Token.create_personal(
        "test-personal-{0}".format(archiver.user.id),
        archiver.user.id,
        scopes=["webhooks:event"],
        is_internal=True,
    ).access_token
    db.session.commit()
    return token


@pytest.fixture()
def headers():
    """Default headers for making requests."""
    return {
        "content-type": "application/json",
        "accept": "application/json",
    }


@pytest.fixture()
def access_token_headers(access_token):
    """Bearer token headers for making requests."""
    return {
        "content-type": "application/json",
        "accept": "application/json",
        "authorization": "Bearer " + access_token,
    }
