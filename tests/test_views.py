# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Views tests."""

import json


def test_send_public_preservations(
    app, client, archiver, headers, access_token_headers
):
    """Test public record preservation events."""
    r = client.get("/records/public_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 0

    payload = json.dumps(
        {
            "pid": "public_pid",
            "revision_id": "1",
            "status": "P",
            "uri": "https://test-archive.org/abcd",
            "path": "/test/archive/aips/abcd",
            "harvest_timestamp": "2024-07-30T23:57:18",
            "archive_timestamp": "2024-07-31T13:34:18",
            "description": {"compliance": "OAIS", "sender": "Preservation Platform"},
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=headers,
        data=payload,
    )
    assert r.status_code == 401

    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 202

    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 409

    r = client.get("/records/public_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1

    r = client.get("/records/public_pid/preservations/latest", headers=headers)
    assert r.status_code == 200
    assert r.json["status"] == "P"
    assert r.json["revision_id"] == 1

    client = archiver.logout(client)
    r = client.get("/records/public_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1

    client = archiver.login(client)
    payload = json.dumps(
        {
            "pid": "public_pid",
            "revision_id": "2",
            "status": "F",
            "harvest_timestamp": "2024-07-31T23:59:18",
            "archive_timestamp": "2024-08-01T18:34:18",
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=payload,
    )
    assert r.status_code == 202

    r = client.get("/records/public_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 2

    r = client.get("/records/public_pid/preservations/latest", headers=headers)
    assert r.status_code == 200
    assert r.json["status"] == "F"
    assert r.json["revision_id"] == 2


def test_send_restricted_preservations(
    app, client, archiver, headers, access_token_headers
):
    """Test restricted recors preservation events."""
    r = client.get("/records/restricted_pid/preservations", headers=headers)
    assert r.status_code == 403

    client = archiver.login(client)
    r = client.get("/records/restricted_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 0

    payload = json.dumps(
        {
            "pid": "restricted_pid",
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
    assert r.status_code == 202

    # Update one field
    updated_payload = json.dumps(
        {
            "pid": "restricted_pid",
            "revision_id": "1",
            "status": "preserved",
            "uri": "https://test-archive.org/abcd",
            "path": "/test/archive/aips/updated_path",
            "harvest_timestamp": "2024-07-31T23:59:18",
            "archive_timestamp": "2024-08-01T18:34:18",
            "description": {"compliance": "OAIS", "sender": "Preservation Platform"},
        }
    )
    r = client.post(
        "hooks/receivers/preservation/events",
        follow_redirects=True,
        headers=access_token_headers,
        data=updated_payload,
    )
    assert r.status_code == 202

    r = client.get("/records/restricted_pid/preservations", headers=headers)
    assert r.status_code == 200
    assert r.json["hits"]["total"] == 1
    assert r.json["hits"]["hits"][0]["path"] == "/test/archive/aips/updated_path"
    assert r.json["hits"]["hits"][0]["status"] == "P"

    client = archiver.logout(client)
    r = client.get("/records/restricted_pid/preservations", headers=headers)
    assert r.status_code == 403
