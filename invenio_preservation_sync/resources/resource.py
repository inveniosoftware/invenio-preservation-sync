# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Preservation Sync module to create REST APIs."""

from flask import g
from flask_resources import (
    Resource,
    from_conf,
    request_parser,
    resource_requestctx,
    response_handler,
    route,
)

from ..errors import ErrorHandlersMixin
from ..proxies import current_preservation_sync_service as service

request_view_args = request_parser(from_conf("request_view_args"), location="view_args")


class PreservationInfoResource(ErrorHandlersMixin, Resource):
    """Preservation Info resource."""

    def __init__(self, config, latest_path=None, list_path=None):
        """Constructor."""
        super(PreservationInfoResource, self).__init__(config)
        self.latest_route = latest_path
        self.list_route = list_path

    def create_url_rules(self):
        """Create the URL rules for the preservation info resource."""
        routes = self.config.routes
        if not self.latest_route:
            self.latest_route = routes["latest"]
        if not self.list_route:
            self.list_route = routes["list"]
        return [
            route("GET", self.latest_route, self.get_latest),
            route("GET", self.list_route, self.get_list),
        ]

    @request_view_args
    @response_handler()
    def get_latest(self):
        """Returns list of preservations for a given record."""
        pid_id = resource_requestctx.view_args["pid_id"]
        preservation = service.read(g.identity, pid_id, latest=True)
        return preservation.to_dict(), 200

    @request_view_args
    @response_handler()
    def get_list(self):
        """Returns list of preservations for a given record."""
        pid_id = resource_requestctx.view_args["pid_id"]
        preservations = service.read(g.identity, pid_id)
        return preservations.to_dict(), 200
