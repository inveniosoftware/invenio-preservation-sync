#
# This file is part of Invenio.
# Copyright (C) 2026 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""change datetime types"""

from invenio_db.utils import (
    update_table_columns_column_type_to_datetime,
    update_table_columns_column_type_to_utc_datetime,
)

# revision identifiers, used by Alembic.
revision = "1770971819"
down_revision = "2e6fbe6998cc"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    update_table_columns_column_type_to_utc_datetime("preservation_info", "created")
    update_table_columns_column_type_to_utc_datetime("preservation_info", "updated")
    update_table_columns_column_type_to_utc_datetime(
        "preservation_info", "harvest_timestamp"
    )
    update_table_columns_column_type_to_utc_datetime(
        "preservation_info", "archive_timestamp"
    )


def downgrade():
    """Downgrade database."""
    update_table_columns_column_type_to_datetime("preservation_info", "created")
    update_table_columns_column_type_to_datetime("preservation_info", "updated")
    update_table_columns_column_type_to_datetime(
        "preservation_info", "harvest_timestamp"
    )
    update_table_columns_column_type_to_datetime(
        "preservation_info", "archive_timestamp"
    )
