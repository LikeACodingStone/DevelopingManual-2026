"""New integration contract, NOT a vendor SDK implementation or recognizer.
A real adapter must be supplied by the application using its licensed SDK.
No fake text/audio result is produced.
"""
from typing import Protocol

class Adapter(Protocol):
    def open(self) -> None: ...
    def start(self) -> None: ...
    def feed(self, pcm: bytes) -> None: ...
    def finish(self) -> object: ...
    def close(self) -> None: ...


def run_session(adapter: Adapter, chunks) -> object:
    """Adapter owns SDK-specific authentication, format checks and release rules.
    close() must tolerate partial open/start failure and release any acquired handle.
    """
    try:
        adapter.open()
        adapter.start()
        for chunk in chunks:
            if not isinstance(chunk, bytes):
                raise TypeError('PCM chunk must be bytes')
            if chunk:
                adapter.feed(chunk)
        return adapter.finish()
    finally:
        adapter.close()
