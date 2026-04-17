"""Configuración de logging profesional para CalcElec"""
import logging
import logging.handlers
import os
import sys


def setup_logging(log_dir=None, level=logging.INFO):
    if log_dir is None:
        log_dir = os.path.join(os.path.expanduser('~'), '.calcElec_logs')
    
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'calcelec.log')
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    return root_logger


def get_logger(name):
    return logging.getLogger(name)
