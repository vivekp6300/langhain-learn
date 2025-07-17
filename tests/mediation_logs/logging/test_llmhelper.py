import os
from logutil.logutil import get_logger

def test_setup_Logging(tmp_path):
    log_dir = tmp_path / "logs"
    logger = get_logger("console")

    # Example usage
    logger.info("This is a console log message.")
    logger.info("This is a file log message.")
    logger.info("This is a JSON log message.")
    logger.error("This is an error message with structlog.")

    assert os.path.exists("tests/logs/app.log")
    assert os.path.exists("tests/logs/logpipe.json")
    with open("tests/logs/app.log", "r") as f:
        assert any("This is a file log message." in line for line in f), "File log message missing"

    with open("tests/logs/logpipe.json", "r") as f:
        assert any('"event": "This is a JSON log message."' in line for line in f), "JSON log message missing"

def test_file_logging(tmp_path):
    log_dir = tmp_path / "logs"
    logger = get_logger("file")
    logger.info("This is a file log message.")
    