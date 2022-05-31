import errno
import subprocess

from freezegun import freeze_time

RUNNING = """
ID   Status  Spawn                   Ready                   Summary
42   Done    yesterday at 17:10 UTC  yesterday at 17:10 UTC  ...
43   Doing
""".lstrip()

DONE = """
ID   Status  Spawn                   Ready                   Summary
42   Done    yesterday at 17:10 UTC  yesterday at 17:10 UTC  ...
43   Done    today at 13:58 UTC      today at 13:58 UTC      ...
""".lstrip()


def test_main(script, args, mocker):
    path_exists = mocker.patch("os.path.exists")
    path_exists.return_value = True

    parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
    parse_args.return_value = args

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout="no changes found"
    )

    assert script.main() == 0
    assert subprocess_run.call_count == 2


def test_main_not_root(script, args, mocker):
    logger_error = mocker.patch("logging.error")
    parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
    parse_args.return_value = args

    get_euid = mocker.patch("os.geteuid")
    get_euid.return_value = 1
    assert script.main() == errno.EACCES
    logger_error.assert_called_once()


def test_main_not_found(script, args, mocker):
    path_exists = mocker.patch("os.path.exists")
    path_exists.return_value = False

    parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
    parse_args.return_value = args

    assert script.main() == errno.ENOENT


def test_main_loop(script, args, mocker):
    time_sleep = mocker.patch("time.sleep")

    path_exists = mocker.patch("os.path.exists")
    path_exists.return_value = True

    args.delay = 0
    parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
    parse_args.return_value = args

    count = 0

    def _subprocess_run(*_args, **_kwargs):
        nonlocal count
        count += 1
        if count == 1:
            return subprocess.CompletedProcess(
                args="", returncode=0, stdout=RUNNING
            )
        if count == 2:
            return subprocess.CompletedProcess(args="", returncode=1)
        return subprocess.CompletedProcess(
            args="", returncode=0, stdout=DONE
        )

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.side_effect = _subprocess_run

    builtins_print = mocker.patch("builtins.print")

    assert script.main() == 0
    builtins_print.assert_called_once()
    time_sleep.assert_called_once()


def test_main_wait_exceeded(script, args, mocker):
    logging_error = mocker.patch("logging.error")
    path_exists = mocker.patch("os.path.exists")
    path_exists.return_value = True

    args.delay = 0
    parse_args = mocker.patch("argparse.ArgumentParser.parse_args")
    parse_args.return_value = args

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value = subprocess.CompletedProcess(
        args="", returncode=0, stdout=RUNNING
    )

    tick = script.MAX_WAIT_TIME * 2 * 60
    with freeze_time("1970-01-01 00:00:00", auto_tick_seconds=tick):
        assert script.main() == errno.ETIMEDOUT

    logging_error.assert_called_once()
