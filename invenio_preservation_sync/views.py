# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Preservation Sync blueprint for Invenio platform."""

from flask import Blueprint, abort, current_app, jsonify
from flask_login import login_required

from invenio_preservation_sync.errors import PermissionDeniedError
from invenio_preservation_sync.proxies import (
    current_preservation_sync_service as service,
)
from invenio_preservation_sync.services.service import PreservationInfoResult


def create_api_blueprint(app):
    """Creates blueprint and registers API endpoints if the integration is enabled."""
    blueprint_api = Blueprint("invenio_preservation_sync_api", __name__)
    register_api_routes(app, blueprint_api)
    return blueprint_api


def register_api_routes(app, blueprint):
    """Register API routes."""

    def generate_list_response(preservations, links=None):
        return jsonify(
            {
                "hits": {
                    "hits": (
                        list(map(PreservationInfoResult.to_json, preservations))
                        if preservations
                        else []
                    ),
                    "total": len(preservations) if preservations else 0,
                },
                "links": links,
            }
        )

    @blueprint.route(app.config.get("PRESERVATION_SYNC_GET_LIST_PATH"), methods=["GET"])
    def get_preservations(id):
        """Returns list of preservations for a given record."""
        try:
            preservations = service.get_by_record_id(pid_id=id)
        except PermissionDeniedError as exc:
            abort(403, str(exc))
        except Exception as exc:
            current_app.logger.exception(str(exc))
            abort(400)
        return generate_list_response(preservations), 200

    @blueprint.route(
        app.config.get("PRESERVATION_SYNC_GET_LATEST_PATH"), methods=["GET"]
    )
    def get_latest_preservation(id):
        """Returns list of preservations for a given record."""
        try:
            preservation = service.get_by_record_id(pid_id=id, latest=True)
        except PermissionDeniedError as exc:
            abort(403, str(exc))
        except Exception as exc:
            current_app.logger.exception(str(exc))
            abort(400)
        if preservation:
            return preservation.to_json(), 200
        else:
            abort(404)
