from pathlib import Path
import tomllib
import tomli_w

from pin_archivist.pin_archivist_config import PinArchivistConfig



class ConfigHandler:

    configFilePath: Path
    configData: dict

    @classmethod
    def loadConfig(cls, configFilePath: Path):
        cls.configFilePath = configFilePath

        with configFilePath.open("rb") as configFile:
            cls.configData = tomllib.load(configFile)

    # def __init__(self, configFilePath: Path):
    #     self.configFilePath = configFilePath

    #     with configFilePath.open("rb") as configFile:
    #         self.configData = tomllib.load(configFile)

    @classmethod
    def getPinArchivistConfig(cls) -> PinArchivistConfig:

        if (archivistConfig := cls.configData.get("pin_archivist", None)) is None:
            return PinArchivistConfig([])

        return PinArchivistConfig(archivistConfig.get("authorized_user_ids", []))
    
    
    @classmethod
    def setPinArchivistConfig(cls, config: PinArchivistConfig):
        cls.configData["pin_archivist"] = {
            "authorized_user_ids": config.authorizedUserIds
        }

        cls.saveConfig()

    
    @classmethod
    def saveConfig(cls):
        with cls.configFilePath.open("wb") as configFile:
            tomli_w.dump(cls.configData, configFile)