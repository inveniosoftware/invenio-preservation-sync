# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Invenio Resources module to create REST APIs."""

from .config import PreservationInfoResourceConfig
from .resource import PreservationInfoResource

__all__ = (
    "PreservationInfoResource",
    "PreservationInfoResourceConfig",
)
