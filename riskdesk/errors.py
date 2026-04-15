from __future__ import annotations


class PacificaAPIError(Exception):
    """Raised when Pacifica REST returns an error or an unexpected payload."""

    def __init__(
        self,
        message: str,
        *,
        http_status: int | None = None,
        body_text: str | None = None,
    ) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.body_text = body_text
