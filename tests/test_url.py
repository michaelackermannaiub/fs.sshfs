# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

import fs
from semantic_version import Version

from . import utils


@unittest.skipIf(utils.fs_version() < Version("2.0.10"), "FS URL params not supported.")
class TestFSURL(unittest.TestCase):

    user = "user"
    pasw = "pass"
    port = 2224

    def test_timeout(self):
        with utils.mock.patch('fs.sshfs.SSHFS', utils.mock.MagicMock()) as magic:
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=1')
            self.assertEqual(magic.call_args[-1]['timeout'], 1)
            fs.open_fs('ssh://user:pass@localhost:2224/?compress=1&timeout=5')
            self.assertEqual(magic.call_args[-1]['timeout'], 5)

    def test_compress(self):
        with utils.mock.patch('fs.sshfs.SSHFS', utils.mock.MagicMock()) as magic:
            fs.open_fs('ssh://user:pass@localhost:2224/?compress=true')
            self.assertEqual(magic.call_args[-1]['compress'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&compress=1')
            self.assertEqual(magic.call_args[-1]['compress'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&compress=0')
            self.assertEqual(magic.call_args[-1]['compress'], False)

    def test_look_for_keys(self):
        with utils.mock.patch('fs.sshfs.SSHFS', utils.mock.MagicMock()) as magic:
            fs.open_fs('ssh://user:pass@localhost:2224/')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?look-for-keys=true')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?look-for-keys=false')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], False)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&look-for-keys=1')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&look-for-keys=0')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], False)

