import socket
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from pathlib import Path

from ppx_py import Settings
from ppx_py.commands import dev

ROOT = Path(__file__).resolve().parents[3]


class DevTests(unittest.TestCase):
    def test_occupied_port_never_launches_an_unrelated_frontend(self):
        with socket.socket() as server:
            server.bind(('127.0.0.1', 0))
            server.listen()
            settings = SimpleNamespace(development=SimpleNamespace(port=server.getsockname()[1]))
            with patch.object(dev, 'find_project_root', return_value=ROOT), patch.object(
                dev, 'load_settings', return_value=settings
            ), patch.object(dev.subprocess, 'Popen') as spawn, patch.object(dev, 'run_project') as run:
                self.assertEqual(dev.run(SimpleNamespace()), 1)
                spawn.assert_not_called()
                run.assert_not_called()

    def test_frontend_uses_configured_port_and_is_cleaned_when_runtime_fails(self):
        settings = Settings.load(ROOT / 'ppx.toml')
        process = Mock()
        with patch.object(dev, 'find_project_root', return_value=ROOT), patch.object(
            dev, 'load_settings', return_value=settings
        ), patch.object(dev.socket, 'create_connection', side_effect=OSError), patch.object(
            dev.subprocess, 'Popen', return_value=process
        ) as spawn, patch.object(dev, '_wait_for_port'), patch.object(
            dev, 'run_project', side_effect=RuntimeError('window failed')
        ), patch.object(dev, '_stop') as stop:
            self.assertEqual(dev.run(SimpleNamespace()), 1)
            command = spawn.call_args.args[0]
            self.assertIn('--strictPort', command)
            self.assertNotIn('--', command)
            self.assertEqual(command[command.index('--port') + 1], str(settings.development.port))
            stop.assert_called_once_with(process)
