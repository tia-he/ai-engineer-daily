import logging


def configure_logging(level: int = logging.INFO) -> None:
    """
    配置全局日志格式。

    由 main.py（应用启动时）以及各个独立脚本（ingest_rss.py、
    generate_ai.py 的 __main__ 入口）分别调用一次，而不是在
    openai_client.py 这类会被其它模块 import 的模块里调用。
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
