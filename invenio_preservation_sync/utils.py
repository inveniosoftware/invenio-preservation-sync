# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utils for Preservation Sync module."""

from flask import current_app, g, url_for

from invenio_preservation_sync.models import PreservationStatus

from .proxies import current_preservation_sync_service as service


def preservation_info_render(record):
    """Render the preservation info."""
    permissions = record.has_permissions_to(["manage"])
    can_manage = permissions.get("can_manage", False)

    pid = record._record.pid.pid_value
    result = service.read(g.identity, pid, latest=True).data

    if not result or (
        result["status"] != PreservationStatus.PRESERVED and not can_manage
    ):
        return []

    title = current_app.config.get(
        "PRESERVATION_SYNC_UI_TITLE", "Preservation Platform"
    )
    url = current_app.config.get("PRESERVATION_SYNC_UI_LINK", result["uri"])
    if can_manage and not current_app.config.get(
        "PRESERVATION_SYNC_UI_MANAGER_LINK_OVERRIDE", True
    ):
        url = result["uri"]
    status = PreservationStatus(result["status"]).name
    logo_path = current_app.config.get("PRESERVATION_SYNC_UI_ICON_PATH", None)

    return [
        {
            "content": {
                "url": url,
                "title": title,
                "subtitle": status,
                "icon": (url_for("static", filename=logo_path) if logo_path else None),
                "section": ("Preserved in"),
            },
        }
    ]
