from collections.abc import Mapping, MutableMapping
from shutil import rmtree, copytree
import os


class DirDict(MutableMapping, Mapping):
    """
        DirDict class implements python dict interface to work with files on disk in specified dir.

        Inherited (mixins):
            Mapping methods(__contains__, keys, items, values, get, __eq__, __ne__)
            MutableMapping methods(pop, popitem, clear, update, setdefault).
    """
    def __new__(cls, dir):
        if not os.path.exists(dir):
            # TODO: maybe better create dir
            raise ValueError("Not exists.")
        if not os.path.isdir(dir):
            raise ValueError("Not a directory.")
        return super().__new__(cls)

    def __init__(self, dir):
        self._dir = os.path.abspath(dir)
        super().__init__()

    def __iter__(self):
        for dir in os.listdir(self._dir):
            yield dir

    def __len__(self):
        return len(os.listdir(self._dir))

    def __getitem__(self, item):
        path = os.path.join(self._dir, item)
        if os.path.isdir(path):
            return DirDict(path)
        elif os.path.isfile(path):
            with open(path, "r") as f:
                string = f.read()
            return string
        else:
            raise KeyError("No such file or directory.")

    def __delitem__(self, key):
        # TODO: how to deal with deleted folder return?
        path = os.path.join(self._dir, key)
        if os.path.isdir(path):
            rmtree(path)
            return None
        elif os.path.isfile(path):
            with open(path, "r") as f:
                text = f.read()
            os.remove(path)
            return text
        else:
            raise KeyError("No such file or directory.")

    def __setitem__(self, key, value):
        path = os.path.join(self._dir, key)
        if os.path.isdir(path):
            rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        if isinstance(value, type(self)):
            copytree(value.dir, path)
        else:
            with open(path, "w") as f:
                f.write(value)

    @property
    def dir(self):
        return self._dir