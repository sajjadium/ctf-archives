import re
from rich.logging import RichHandler
from rich._null_file import NullFile
from rich.traceback import Traceback


class ObjDict:
    def __init__(self, d={}):
        self.__dict__['_data'] = d # Avoiding Recursion errors on __getitem__

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        return None

    def __contains__(self, key):
        return key in self._data

    def __setattr__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.__dict__["_data"].clear()
        del self.__dict__['_data']
        del self

    def __repr__(self):
        return f"ObjDict object at <{hex(id(self))}>"

    def __iter__(self):
        return iter(self._data)
    
class TruncatedStringHandler(RichHandler):
    def __init__(self, max_length=256):
        super().__init__()
        self.max_length = max_length

    def emit(self, record) -> None: 
        """Invoked by logging, taken from rich.logging.RichHandler"""
        """NOTE: THIS IS NOT PART OF THE CHALLENGE. DO NOT WASTE TIME"""
        record.msg = re.sub(r"\)\d+.", ")", record.msg)
        message = self.format(record)
        traceback = None
        if (
            self.rich_tracebacks
            and record.exc_info
            and record.exc_info != (None, None, None)
        ):
            exc_type, exc_value, exc_traceback = record.exc_info
            assert exc_type is not None
            assert exc_value is not None
            traceback = Traceback.from_exception(
                exc_type,
                exc_value,
                exc_traceback,
                width=self.tracebacks_width,
                extra_lines=self.tracebacks_extra_lines,
                theme=self.tracebacks_theme,
                word_wrap=self.tracebacks_word_wrap,
                show_locals=self.tracebacks_show_locals,
                locals_max_length=self.locals_max_length,
                locals_max_string=self.locals_max_string,
                suppress=self.tracebacks_suppress,
            )
            message = record.getMessage()
            if self.formatter:
                record.message = record.getMessage()
                formatter = self.formatter
                if hasattr(formatter, "usesTime") and formatter.usesTime():
                    record.asctime = formatter.formatTime(record, formatter.datefmt)
                message = formatter.formatMessage(record)

        message_renderable = self.render_message(record, message)
        
        if len(message_renderable) > self.max_length:
            message_renderable = message_renderable[:self.max_length - 3] + "..."
        
        log_renderable = self.render(
            record=record, traceback=traceback, message_renderable=message_renderable
        )
        
        if isinstance(self.console.file, NullFile):
            self.handleError(record)
        else:
            try:
                self.console.print(log_renderable)
            except Exception:
                self.handleError(record)
                