from dataclasses import dataclass

@dataclass
class PinArchivistConfig:
    authorizedUserIds: list[int]