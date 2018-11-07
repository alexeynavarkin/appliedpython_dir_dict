from unittest import TestCase
import os, shutil

from dirdict import DirDict


class DirBaseTest(TestCase):
    def setUp(self):
        os.makedirs("test_dir/1_dir/2_dir")
        with open("test_dir/first_level.txt", "w") as f:
            f.write("First level text")
        with open("test_dir/1_dir/second_level.txt", "w") as f:
            f.write("Second level text")


    def tearDown(self):
        try:
            shutil.rmtree("test_dir")
        except Exception:
            pass

    def test_list(self):
        dir = DirDict("test_dir")

        self.assertEqual(['1_dir', 'first_level.txt'],list(dir))

    def test_nested_read(self):
        dir = DirDict("test_dir")

        self.assertEqual("First level text",dir['first_level.txt'])
        self.assertEqual("Second level text", dir['1_dir']['second_level.txt'])

    def test_modify(self):
        dir = DirDict("test_dir")
        dir['first_level.txt'] = "Test text"
        dir['1_dir']['second_level.txt'] = "Test text"

        self.assertEqual("Test text", dir['first_level.txt'])
        self.assertEqual("Test text", dir['1_dir']['second_level.txt'])

    def test_copy(self):
        dir1 = DirDict("test_dir")
        dir2 = DirDict("test_dir/1_dir")

        dir1["1_dir_copy"] = dir2
        self.assertEqual(['2_dir', 'second_level.txt'], list(dir1["1_dir_copy"]))

    def test_del(self):
        dir = DirDict("test_dir")
        dir.pop("first_level.txt")
        del(dir["1_dir"])
        self.assertEqual(0, len(dir))