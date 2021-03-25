from unittest.mock import MagicMock, patch

from todolist import __version__
from todolist.run import run


def test_version():
    assert __version__ == "0.1.0"


def test_run():
    app_mock = MagicMock()

    with patch("todolist.run.create_app", return_value=app_mock):
        run()

        app_mock.run.assert_called()
