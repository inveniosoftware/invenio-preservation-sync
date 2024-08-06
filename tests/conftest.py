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

import pytest
from invenio_app.factory import create_app as _create_app


@pytest.fixture(scope="module")
def app_config(app_config):
    """Application config override."""
    app_config["PRESERVATION_SYNC_INTEGRATION_ENABLED"] = True
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app


@pytest.fixture()
def test_user(app, db):
    """Creates a test user."""
    datastore = app.extensions["security"].datastore
    user = datastore.create_user(
        email="info@inveniosoftware.org",
        password="tester",
    )

    db.session.commit()
    return user


@pytest.fixture()
def tester_id(test_user):
    """Returns tester id."""
    return test_user.id
