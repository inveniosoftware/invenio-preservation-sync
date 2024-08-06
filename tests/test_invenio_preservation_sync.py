# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

import json
from contextlib import contextmanager

from flask import Flask, appcontext_pushed, g
from invenio_webhooks.models import Event

from invenio_preservation_sync import InvenioPreservationSync


def test_version():
    """Test version import."""
    from invenio_preservation_sync import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioPreservationSync(app)
    assert "invenio-preservation-sync" in app.extensions

    app = Flask("testapp")
    ext = InvenioPreservationSync()
    assert "invenio-preservation-sync" not in app.extensions
    ext.init_app(app)
    assert "invenio-preservation-sync" in app.extensions


"""
def test_receiver(app, db, test_user, tester_id):
    #Test preservation receiver.
    payload = json.dumps(
        {
            "pid": "rhtwj-hee56",
            "revision_id": "1",
            "status": "P",
            "uri": "https://oais-registry-test.web.cern.ch/abcd",
            "path": "/eos/user/o/oais/luteus/aips/abcd",
            "harvest_timestamp": "2024-07-30T23:57:18",
            "archive_timestamp": "2024-07-31T23:57:18",
            "description": {"compliance": "OAIS", "sender": "OAIS Platform"},
        }
    )
    headers = [("Content-Type", "application/json")]

    with app.test_request_context(headers=headers, data=payload):
        event = Event.create(receiver_id="preservation", user_id=tester_id)
        # Add event to session. Otherwise defaults are not added (e.g. response and response_code)
        db.session.add(event)
        db.session.commit()
        event.process()

    assert event.response_code == 202
    # TODO validate PreservationInfo object created
"""
