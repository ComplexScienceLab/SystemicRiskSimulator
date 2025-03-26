"""
日志记录器工具
"""

from SystemicRiskSimulator.external_packages import logging, Union, Path, functools, sqlite3


def record_work_state(id_experiment: int, state_column: str, state_value: str, folderpath_experiments_output_log: Path):
    """
    记录本次实验作业的状态

    Args:
        id_experiment (int): 实验组 id
        state_column (str): 状态列名称
        state_value (str): 状态值
        folderpath_experiments_output_log (Path): 实验组输出日志文件夹路径

    Returns:
          None
    """
    conn = sqlite3.connect(Path(folderpath_experiments_output_log, "experiments_works_status.db"))
    c = conn.cursor()
    c.execute(f"UPDATE experiments SET {state_column} = ? WHERE exp_id = ?", (state_value, id_experiment))
    conn.commit()
    conn.close()
    pass  # function


def log_decorator(filepath_log: Union[str, Path], logger_name=None, level_to_logFileHandler=logging.DEBUG, level_to_logConsoleHandler=logging.INFO):
    """
    日志装饰器 #DEBUG 尚未测试

    Args:
        filepath_log (Optional[str, Path]): 日志文件路径
        logger_name (str): 日志记录器名称
        level_to_logFileHandler (int): 文件处理器级别。默认为 DEBUG
        level_to_logConsoleHandler (int): 控制台处理器级别为 INFO

    Returns:
        function: 装饰器
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取 logger
            logger = logging.getLogger(logger_name or func.__name__)

            # 创建一个 file handler，并设置日志级别
            log_file_handler = logging.FileHandler(Path(filepath_log, f"{func.__name__}.txt"))
            log_file_handler.setLevel(level_to_logFileHandler)

            # 创建一个 stream handler，并设置日志级别
            log_console_handler = logging.StreamHandler()
            log_console_handler.setLevel(level_to_logConsoleHandler)

            # 将这两个 handler 添加到 logger 中
            logger.addHandler(log_file_handler)
            logger.addHandler(log_console_handler)

            # 执行函数
            result = func(*args, **kwargs)

            # 关闭 logger
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)

            return result

        return wrapper

    return decorator

    pass  # function


def get_logger(filepath_log: Union[str, Path], logger_name=None, level_to_logFileHandler=logging.DEBUG, level_to_logConsoleHandler=logging.INFO) -> logging.Logger:
    """
    设置日志记录器

    Args:
        filepath_log (Optional[str, Path]): 日志文件路径
        logger_name (str): 日志记录器名称
        level_to_logFileHandler (int): 文件处理器级别。默认为 DEBUG
        level_to_logConsoleHandler (int): 控制台处理器级别为 INFO

    Returns:
        logging.Logger: 日志记录器
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，并设置级别为 DEBUG
    log_file_handler = logging.FileHandler(filepath_log)
    log_file_handler.setLevel(level_to_logFileHandler)

    # 创建控制台处理器，并设置级别为 DEBUG
    log_console_handler = logging.StreamHandler()
    log_console_handler.setLevel(level_to_logConsoleHandler)

    # 将文件处理器和控制台处理器添加到 logger
    logger.addHandler(log_file_handler)
    logger.addHandler(log_console_handler)

    return logger
    pass  # function


def close_logger(logger: logging.Logger):
    """
    关闭日志记录器

    Args:
        logger (logging.Logger): 日志记录器
    """
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
    pass  # function


def log_message(message: str, filepath_log: Union[str, Path], logger_name=None, is_enable_multiprocessing_for_run_model: bool = True, level_to_logFileHandler=logging.DEBUG, level_to_logConsoleHandler=logging.INFO):
    """
    记录日志消息

    Args:
        message (str): 日志消息
        filepath_log (Optional[str, Path]): 日志文件路径
        logger_name (str): 日志记录器名称
        is_enable_multiprocessing_for_run_model (bool): 是否启用多进程
        level_to_logFileHandler (int): 文件处理器级别。默认为 DEBUG
        level_to_logConsoleHandler (int): 控制台处理器级别为 INFO

    Returns:
        None
    """
    if is_enable_multiprocessing_for_run_model:
        logger = get_logger(filepath_log, logger_name, level_to_logFileHandler, level_to_logConsoleHandler)
        logger.info(message)
        close_logger(logger)
    else:
        filepath_log, logger_name = None, None
        logging.info(message)
        pass  # if
    pass  # function


def log_listener(queue):
    """
    日志监听器。监听队列中的日志消息，并处理。

    Args:
        queue (Queue): 队列

    Returns:
        None

    """
    while True:
        try:
            record = queue.get()
            if record is None:
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)
        except Exception:
            import sys, traceback
            print('Error in log listener:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    pass  # function
