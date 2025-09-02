from enum import Enum


class ListRepoMetadataOrderBy(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
