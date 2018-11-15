from collections.abc import Mapping, MutableMapping
from shutil import rmtree, copytree
from os import path, remove, listdir


class DirDict(MutableMapping):
    """
        DirDict class implements python dict interface to work with files on disk in specified dir.

        Inherited (mixins):
            Mapping methods(__contains__, keys, items, values, get, __eq__, __ne__)
            MutableMapping methods(pop, popitem, clear, update, setdefault).
    """
    def __new__(cls, folder_path):
        if not path.exists(folder_path):
            # TODO: maybe better create dir
            raise ValueError("Not exists.")
        if not path.isdir(folder_path):
            raise ValueError("Not a directory.")
        return super().__new__(cls)

    def __init__(self, folder_path):
        self._dir = path.abspath(folder_path)
        super().__init__()

    def __iter__(self):
        for obj in listdir(self._dir):
            yield obj

    def __len__(self):
        return len(listdir(self._dir))

    def __getitem__(self, item):
        item_path = path.join(self._dir, item)
        if path.isdir(item_path):
            return DirDict(item_path)
        elif path.isfile(item_path):
            with open(item_path, "r") as f:
                data = f.read()
            return data
        else:
            raise KeyError("No such file or directory.")

    def __delitem__(self, key):
        item_path = path.join(self._dir, key)
        if path.isdir(item_path):
            rmtree(item_path)
        elif path.isfile(item_path):
            remove(item_path)
        else:
            raise KeyError("No such file or directory.")

    def __setitem__(self, key, value):
        item_path = path.join(self._dir, key)
        if path.isdir(item_path):
            rmtree(item_path)
        elif path.isfile(item_path):
            remove(item_path)
        if isinstance(value, type(self)):
            copytree(value.dir, item_path)
        else:
            with open(item_path, "w") as f:
                f.write(value)

    @property
    def dir(self):
        return self._dir
