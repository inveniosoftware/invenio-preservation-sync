# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Preservation Info Resource Configuration."""

import marshmallow as ma
from flask_resources import JSONSerializer, ResourceConfig, ResponseHandler


class PreservationInfoResourceConfig(ResourceConfig):
    """Preservation Info resource config."""

    blueprint_name = "preservations"
    url_prefix = "/"
    routes = {
        "latest": "/records/<pid_id>/preservations/latest",
        "list": "/records/<pid_id>/preservations",
    }

    request_view_args = {
        "pid_id": ma.fields.String(),
    }

    response_handlers = {"application/json": ResponseHandler(JSONSerializer())}
