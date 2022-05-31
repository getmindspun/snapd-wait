def test_process_line_bad_line(script, mocker):
    logging_error = mocker.patch("logging.error")
    assert script.process_line("...") is True
    logging_error.assert_called_once()


def test_process_line_bad_status(script, mocker):
    logging_error = mocker.patch("logging.error")
    assert script.process_line("42 ??? unknown") is True
    logging_error.assert_called_once()
