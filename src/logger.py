import logging
import seqlog

seqlog.configure_from_dict(
    {
        "version": 1,
        "handlers": {
            "seq": {
                "class": "seqlog.structured_logging.SeqLogHandler",
                "formatter": "plain",
                "server_url": "http://localhost:5341",
                "api_key": "",
                "batch_size": 1,
                "auto_flush_timeout": 1,
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "filename": "app.log",
                "mode": "a",
            },
        },
        "formatters": {
            "plain": {
                "format": "{timestamp} [{level}] {message} ({logger})",
                "style": "{",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["seq", "console", "file"],
        },
    }
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
