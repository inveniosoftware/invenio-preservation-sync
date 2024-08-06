# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Preservation Sync blueprint for Invenio platform."""

from flask import Blueprint, abort, current_app, g, jsonify
from flask_login import login_required

from invenio_preservation_sync.api import PreservationInfoAPI
from invenio_preservation_sync.errors import MissingConfigError
from invenio_preservation_sync.utils import get_mandatory_config


def create_api_blueprint(app):
    """Creates blueprint and registers API endpoints if the integration is enabled."""
    blueprint_api = Blueprint("invenio_preservation_sync_api", __name__)
    if app.config.get("PRESERVATION_SYNC_INTEGRATION_ENABLED", False):
        register_api_routes(app, blueprint_api)
    return blueprint_api


def generate_response(result):
    """Generate response structure."""
    return {
        "hits": {
            "hits": PreservationInfoAPI.convert_to_dict(result),
            "total": len(result),
        }
    }


def register_api_routes(app, blueprint):
    """Register API routes."""
    preservation_info_api = PreservationInfoAPI()

    @login_required
    @blueprint.route(
        get_mandatory_config(app, "PRESERVATION_SYNC_GET_LIST_PATH"), methods=["GET"]
    )
    def get_preservations(id):
        """Returns list of preservations for a given record."""
        try:
            perm_policy = get_mandatory_config(
                app, "PRESERVATION_SYNC_PERMISSION_POLICY"
            )
            pid_resolver = get_mandatory_config(app, "PRESERVATION_SYNC_PID_RESOLVER")

            record_uuid = pid_resolver(id)

            if not perm_policy.can_read(g.identity, record_uuid):
                current_app.logger.exception(
                    "Unauthorized to read the record's Preservation Info"
                )
                abort(403)

            preservations = preservation_info_api.get_by_record_id(record_uuid).all()
        except Exception as exc:
            current_app.logger.exception(str(exc))
            abort(400)
        return generate_response(preservations), 200

    @login_required
    @blueprint.route(
        get_mandatory_config(app, "PRESERVATION_SYNC_GET_LATEST_PATH"), methods=["GET"]
    )
    def get_latest_preservation(id):
        """Returns list of preservations for a given record."""
        try:
            perm_policy = get_mandatory_config(
                app, "PRESERVATION_SYNC_PERMISSION_POLICY"
            )
            pid_resolver = get_mandatory_config(app, "PRESERVATION_SYNC_PID_RESOLVER")

            record_uuid = pid_resolver(id)

            if not perm_policy.can_read(g.identity, record_uuid):
                current_app.logger.exception(
                    "Unauthorized to read the record's Preservation Info"
                )
                abort(403)

            preservation = preservation_info_api.get_latest_by_record_id(record_uuid)
        except Exception as exc:
            current_app.logger.exception(str(exc))
            abort(400)
        return jsonify(PreservationInfoAPI.convert_to_dict(preservation)), 200
