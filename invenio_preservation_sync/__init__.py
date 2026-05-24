# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Invenio module that adds preservation sync integration to the platform.."""

from .ext import InvenioPreservationSync

__version__ = "0.3.0"

__all__ = ("__version__", "InvenioPreservationSync")
