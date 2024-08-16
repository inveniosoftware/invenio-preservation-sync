# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Receiver tests."""

import json


def test_send_bad_preservations(app, client, archiver, access_token_headers):
    """Test bad preservation event request."""
    client = archiver.login(client)

    payload = json.dumps(
        {
            "pid": "not_existing_pid",
            "revision_id": "1",
            "status": "I",
            "uri": "https://test-archive.org/abcd",
            "path": "/test/archive/aips/abcd",
            "harvest_timestamp": "2024-07-31T23:59:18",
            "archive_timestamp": "2024-08-01T18:34:18",
            "description": {"compliance": "OAIS", "sender": "Preservation Platform"},
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400

    payload = json.dumps({"pid": "restricted_pid", "revision_id": "1"})
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400

    payload = json.dumps(
        {"pid": "restricted_pid", "revision_id": "1", "status": "invalid"}
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 400
