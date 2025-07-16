import logging
import sys
import os
import traceback
from typing import Optional, Dict, Any, Callable, Union
from datetime import datetime, timezone
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Error codes for different types of errors
class ErrorCodes:
    CONFIG_INVALID = "CONFIG_001"
    CONFIG_MISSING = "CONFIG_002"
    CONFIG_ACCESS_FAILED = "CONFIG_003"
    DATA_PROCESSING_FAILED = "DATA_001"
    DATA_VALIDATION_FAILED = "DATA_002"
    DEPENDENCY_ANALYSIS_FAILED = "DEPS_001"
    RESOURCE_ACCESS_FAILED = "RES_001"
    RESOURCE_CLEANUP_FAILED = "RES_002"
    VALIDATION_FAILED = "VAL_001"
    UNKNOWN_ERROR = "UNKNOWN_001"

class ConfigError(Exception):
    """Raised for configuration-related errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.CONFIG_INVALID, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class DataProcessingError(Exception):
    """Raised for data processing errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DATA_PROCESSING_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class DependencyAnalysisError(Exception):
    """Raised for dependency analysis errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DEPENDENCY_ANALYSIS_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class ValidationError(Exception):
    """Raised for validation errors in data or configuration."""
    def __init__(self, message: str, error_code: str = ErrorCodes.VALIDATION_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class ResourceError(Exception):
    """Raised for resource access or cleanup errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.RESOURCE_ACCESS_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class StatsProcessingError(Exception):
    """Raised for statistics processing errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DATA_PROCESSING_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class LanguageMappingError(Exception):
    """Raised for language mapping errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DATA_PROCESSING_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class SvgGenerationError(Exception):
    """Raised for SVG generation errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DATA_PROCESSING_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class AnalyticsError(Exception):
    """Raised for analytics processing errors."""
    def __init__(self, message: str, error_code: str = ErrorCodes.DATA_PROCESSING_FAILED, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc)

class SensitiveDataFilter(logging.Filter):
    """Enhanced filter to remove sensitive data from logs."""
    def __init__(self):
        super().__init__()
        self.sensitive_keys = {
            'password', 'token', 'secret', 'key', 'api_key', 'auth', 
            'credential', 'private', 'access', 'bearer', 'authorization'
        }
        self.sensitive_patterns = [
            r'[a-zA-Z0-9]{32,}',  # Long alphanumeric strings (likely tokens)
            r'ghp_[a-zA-Z0-9]{36}',  # GitHub personal access tokens
            r'sk-[a-zA-Z0-9]{48}',  # OpenAI API keys
        ]

    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            msg = record.msg
            for key in self.sensitive_keys:
                if key in msg.lower():
                    msg = msg.replace(key, f'<{key.upper()}_REDACTED>')
            record.msg = msg
        return True

def validate_log_level(level: str) -> int:
    """Validate and return log level."""
    valid_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    level_upper = level.upper()
    if level_upper not in valid_levels:
        raise ValueError(f"Invalid log level: {level}. Valid levels: {list(valid_levels.keys())}")
    return valid_levels[level_upper]

def setup_logging(
    log_level: Optional[int] = None,
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    use_json: bool = False,
    include_timestamp: bool = True,
    max_log_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Set up logging for the application with enhanced features.
    Args:
        log_level: Logging level (defaults to INFO, can be overridden by LOG_LEVEL env var)
        log_file: Optional path to a log file
        log_to_console: Whether to log to the console (stderr)
        use_json: Whether to use JSON format for structured logging
        include_timestamp: Whether to include timestamps in log messages
        max_log_size: Maximum size of log file before rotation (bytes)
        backup_count: Number of backup log files to keep
    """
    # Get a basic logger for setup messages
    basic_logger = logging.getLogger(__name__)
    
    # Validate log level
    if log_level is None:
        env_level = os.environ.get('LOG_LEVEL', 'INFO')
        try:
            log_level = validate_log_level(env_level)
        except ValueError as e:
            basic_logger.warning(f"Invalid log level '{env_level}': {e}. Using INFO level.")
            log_level = logging.INFO

    handlers: list[logging.Handler] = []
    
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stderr)
        handlers.append(console_handler)
    
    if log_file:
        # Validate log file path
        log_path = Path(log_file)
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            # Use rotating file handler for better log management
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=max_log_size, 
                backupCount=backup_count,
                encoding='utf-8'
            )
            handlers.append(file_handler)
        except Exception as e:
            basic_logger.warning(f"Could not set up file logging: {e}", extra={'log_file': log_file})

    # Set up formatter
    if use_json:
        try:
            from pythonjsonlogger import jsonlogger
            formatter = jsonlogger.JsonFormatter(
                fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        except ImportError:
            # Fallback to standard formatter if json logger not available
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
    else:
        if include_timestamp:
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')

    # Apply formatter and filter to all handlers
    for handler in handlers:
        handler.setFormatter(formatter)
        handler.addFilter(SensitiveDataFilter())

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers or [logging.StreamHandler(sys.stderr)],
        force=True  # Ensure configuration is applied
    )
    
    # Log initialization
    logger = logging.getLogger(__name__)
    logger.debug(
        "Logging initialized",
        extra={
            'log_level': logging.getLevelName(log_level),
            'log_file': log_file,
            'console_logging': log_to_console,
            'json_format': use_json,
            'timestamp_included': include_timestamp,
            'max_log_size_mb': max_log_size // (1024 * 1024),
            'backup_count': backup_count
        }
    )

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Global exception handler for uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger = logging.getLogger(__name__)
    logger.critical(
        "Uncaught exception",
        extra={
            'exception_type': exc_type.__name__,
            'exception_message': str(exc_value),
            'traceback': ''.join(traceback.format_tb(exc_traceback))
        },
        exc_info=(exc_type, exc_value, exc_traceback)
    )

def log_and_raise(
    exception: Exception, 
    logger: Optional[logging.Logger] = None,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log the exception with context and raise it.
    Args:
        exception: The exception to log and raise
        logger: Optional logger to use (defaults to root logger)
        context: Additional context to include in the log
    """
    if logger is None:
        logger = logging.getLogger()
    
    # Add context to exception if it supports it
    if hasattr(exception, 'context') and context:
        exception.context.update(context)
    
    # Prepare log message with context
    log_data = {
        'exception_type': type(exception).__name__,
        'exception_message': str(exception),
        'error_code': getattr(exception, 'error_code', ErrorCodes.UNKNOWN_ERROR),
        'context': getattr(exception, 'context', context or {}),
        'timestamp': getattr(exception, 'timestamp', datetime.now(timezone.utc)).isoformat()
    }
    
    logger.error(
        f"Exception occurred: {exception}",
        extra=log_data,
        exc_info=True
    )
    raise exception

def with_error_context(context: Dict[str, Any]):
    """
    Decorator to add context to exceptions.
    Args:
        context: Context to add to any exceptions raised
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Add context to the exception
                if hasattr(e, 'context'):
                    e.context.update(context)
                else:
                    e.context = context
                raise
        return wrapper
    return decorator

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    Args:
        name: Logger name
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def setup_global_exception_handling():
    """Set up global exception handling."""
    sys.excepthook = global_exception_handler

def graceful_shutdown(signum=None, frame=None):
    """Handle graceful shutdown."""
    logger = logging.getLogger(__name__)
    logger.info("Shutting down gracefully...")
    sys.exit(0) 