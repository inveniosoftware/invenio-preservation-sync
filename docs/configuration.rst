..
    SPDX-FileCopyrightText: 2024 CERN.
    SPDX-License-Identifier: MIT


Configuration
=============

.. automodule:: invenio_preservation_sync.config
   :members:


To enable the UI element in the External resources side bar element, the following has to be added to the instance configuration:

.. code-block:: python

    from invenio_preservation_sync.utils import (
        preservation_info_render,
    )

    APP_RDM_RECORD_LANDING_PAGE_EXTERNAL_LINKS = [
        {"id": "preservation", "render": preservation_info_render},
    ]
