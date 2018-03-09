from src.config import process_dir
from src.core.crops import Crop
from src.utils.registry import get_registry


class Core:
    def __init__(self, config_directory: str):
        self.registry = get_registry()
        self.init_configs(config_directory)
        self.init_crops(self.registry.configs)

    def init_configs(self, path: str):
        self.registry.configs = process_dir(path)

    def init_crops(self, config):
        self.registry.crops = {}
        for crop_name, crop_data in config.crops.to_dict().items():
            self.registry.crops[crop_name] = Crop(**crop_data)
