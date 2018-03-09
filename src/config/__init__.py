import os

from src.config.error import ConfigurationError, ConfigFormatError
from src.config.readers import readers


class ConfigContainer(object):
    def __init__(self, data=None):
        if data:
            for key, value in data.items():
                if isinstance(value, dict):
                    setattr(self, key, ConfigContainer(value))
                elif isinstance(value, list):
                    setattr(self, key, container_from_list(value))
                else:
                    setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item, None)

    def items(self):
        return self.__dict__.items()

    def to_dict(self):
        result = {}
        for key, value in self.items():
            if isinstance(value, ConfigContainer):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = dict_from_list(value)
            elif isinstance(value, tuple):
                result[key] = dict_from_list(value)
            else:
                result[key] = value

        return result


class ImmutableConfigContainer(ConfigContainer):
    def __init__(self, data=None):
        if data:
            for key, value in data.items():
                if isinstance(value, dict) or isinstance(value, ConfigContainer):
                    super(ImmutableConfigContainer, self).__setattr__(key, ImmutableConfigContainer(value))
                elif isinstance(value, list):
                    super(ImmutableConfigContainer, self).__setattr__(key, container_from_list(value, True))
                else:
                    super(ImmutableConfigContainer, self).__setattr__(key, value)

    def __setattr__(self, name, value):
        raise TypeError("'%s' object does not support attribute setting" % self.__class__.__name__)


def container_from_list(data, immutable=False):
    result = []
    cls = ImmutableConfigContainer if immutable else ConfigContainer

    for item in data:
        if isinstance(item, dict) or isinstance(item, ConfigContainer):
            result.append(cls(item))
        elif isinstance(item, list):
            result.append(container_from_list(item, immutable))
        else:
            result.append(item)

    return tuple(result) if immutable else result


def dict_from_list(data):
    result = list()
    for item in data:
        if isinstance(item, list):
            result.append(dict_from_list(item))
        if isinstance(item, ConfigContainer):
            result.append(item.to_dict())
        else:
            result.append(item)

    return result


def parse_file(file_path):
    fmt = os.path.splitext(file_path)[1][1:].lower()
    if fmt not in readers:
        raise ConfigurationError('Unsupported configuration format')

    if not check_file_path(file_path):
        raise ConfigurationError('Can not open configuration file (%s)' % file_path)

    reader = readers[fmt]
    data = reader.from_file(file_path)

    return data


def parse_config(cfg_path):
    config = ConfigContainer(parse_file(cfg_path))
    return ImmutableConfigContainer(config)


def check_file_path(path, mode='r'):
    """
    Check whether a path is valid
    @param path: Filepath
    @type path: basestring
    @param mode: how the file is to be opened
    @type mode: basestring
    @return: True if file path is valid else - False
    @rtype: bool
    """

    if path is None:  # in case if path is not set in config file
        return True

    real_path = os.path.realpath(path)
    if not os.path.basename(real_path):
        return False

    try:
        fp = open(real_path, mode)
        fp.close()
    except IOError:
        return False

    return True


def process_dir(path: str):
    data = {}
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise ConfigurationError('Provided path `{0}` is not a directory'.format(path))
    for elem in os.listdir(path):
        fullpath_elem = os.path.join(path, elem)
        if os.path.isdir(fullpath_elem):
            data[elem] = process_dir(fullpath_elem)
            continue
        if not elem.endswith('.xml'):
            continue  # this file is not config
        data[os.path.splitext(elem)[0]] = parse_config(fullpath_elem)
    return ImmutableConfigContainer(data)
