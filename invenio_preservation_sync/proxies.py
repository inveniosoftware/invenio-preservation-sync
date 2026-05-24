# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Proxy for current previewer."""

from flask import current_app
from werkzeug.local import LocalProxy

current_preservation_sync = LocalProxy(
    lambda: current_app.extensions["invenio-preservation-sync"]
)
"""Helper proxy to access the Preservation Sync extension object. """

current_preservation_sync_service = LocalProxy(
    lambda: current_app.extensions["invenio-preservation-sync"].service
)
"""Helper proxy to access the Preservation Sync service. """
