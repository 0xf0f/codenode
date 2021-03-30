from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .writer import Writer


class Settings:
    def __init__(self):
        self.default_indent = '    '
        self._default_writer: 'Writer' = None

    @property
    def default_writer(self) -> 'Writer':
        if self._default_writer is None:
            from .writer import Writer
            self._default_writer = Writer()

        return self._default_writer

    @default_writer.setter
    def default_writer(self, writer: 'Writer'):
        self._default_writer = writer


settings = Settings()
