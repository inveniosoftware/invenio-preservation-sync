# SPDX-FileCopyrightText: 2024 CERN.
# SPDX-License-Identifier: MIT

"""Configs for the service layer to process the Preservation Sync requests."""

from ..models import PreservationInfoModel
from .permissions import DefaultPreservationInfoPermissionPolicy
from .results import PreservationInfoItem, PreservationInfoList
from .schemas import PreservationInfoSchema


class PreservationInfoServiceConfig(object):
    """Service factory configuration."""

    result_item_cls = PreservationInfoItem
    result_list_cls = PreservationInfoList
    permission_policy_cls = DefaultPreservationInfoPermissionPolicy
    schema = PreservationInfoSchema()

    record_cls = PreservationInfoModel
