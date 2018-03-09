import argparse

# LOCALHOST = '127.0.0.1'
# 
# parser = argparse.ArgumentParser()
# parser.add_argument('config', help='Config', nargs='?')
# parser.add_argument('--client', help='Client mode', action='store_true')
# parser.add_argument('--bind-address', help='IP address to bind to', default=LOCALHOST)
# options = parser.parse_args()
# 
# print(options)
from src.core import Core
from src.utils.registry import get_registry

core = Core(config_directory='./data')
print('Crops:', get_registry().crops)
print(get_registry().configs.to_dict())