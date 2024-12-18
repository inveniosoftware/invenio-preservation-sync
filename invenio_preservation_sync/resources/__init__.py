# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Preservation-Sync is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Resources module to create REST APIs."""

from .config import PreservationInfoResourceConfig
from .resource import PreservationInfoResource

__all__ = (
    "PreservationInfoResource",
    "PreservationInfoResourceConfig",
)
