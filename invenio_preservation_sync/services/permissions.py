# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Permissions for the service layer to process the Preservation Sync requests."""

from flask_principal import ActionNeed
from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import Generator, SystemProcess

archiver_action = ActionNeed("archiver")


class Archiver(Generator):
    """Allows system_process role."""

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [archiver_action]

    def query_filter(self, identity=None, **kwargs):
        """Query filter for can_search permission."""
        raise NotImplementedError()


class DefaultPreservationInfoPermissionPolicy(BasePermissionPolicy):
    """Default permission policy to read and write the PreservationInfo."""

    can_create = [Archiver(), SystemProcess()]
    can_read = [Archiver(), SystemProcess()]
