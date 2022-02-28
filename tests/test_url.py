# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

import fs
from semantic_version import Version
import paramiko

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
            self.assertEqual(magic.call_args[-1]['look_for_keys'], None)
            fs.open_fs('ssh://user:pass@localhost:2224/?look-for-keys=true')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?look-for-keys=false')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], False)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&look-for-keys=1')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], True)
            fs.open_fs('ssh://user:pass@localhost:2224/?timeout=5&look-for-keys=0')
            self.assertEqual(magic.call_args[-1]['look_for_keys'], False)

    def test_interaction_between_pkey_and_look_for_keys(self):
        with utils.mock.patch.object(paramiko.SSHClient, "get_transport", return_value=utils.mock.Mock()):
            with utils.mock.patch.object(paramiko.SSHClient, "open_sftp", return_value=utils.mock.Mock()):
                with utils.mock.patch.object(paramiko.SSHClient, "connect") as patched_connect:
                    fs.open_fs("ssh://user:pass@localhost:2224/")
                    _, kwargs = patched_connect.call_args
                    self.assertEqual(kwargs["look_for_keys"], True)

                with utils.mock.patch.object(paramiko.SSHClient, "connect") as patched_connect:
                    fs.open_fs("ssh://user:pass@localhost:2224/?pkey=path-to-pkey")
                    _, kwargs = patched_connect.call_args
                    # FIXME: I would expect this to be False
                    # Based on the documentation and https://github.com/althonos/fs.sshfs/issues/52#issuecomment-1054152600
                    self.assertEqual(kwargs["look_for_keys"], True)

                with utils.mock.patch.object(paramiko.SSHClient, "connect") as patched_connect:
                    fs.open_fs("ssh://user:pass@localhost:2224/?pkey=path-to-pkey&look-for-keys=True")
                    _, kwargs = patched_connect.call_args
                    self.assertEqual(kwargs["look_for_keys"], True)

                with utils.mock.patch.object(paramiko.SSHClient, "connect") as patched_connect:
                    fs.open_fs("ssh://user:pass@localhost:2224/?pkey=path-to-pkey&look-for-keys=False")
                    _, kwargs = patched_connect.call_args
                    self.assertEqual(kwargs["look_for_keys"], False)
