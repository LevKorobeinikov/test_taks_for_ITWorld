from typing import Any, Dict

from app.constants import (
    CONTENT_TEXT_MAX_LENGTH,
    FIELD_CONTENT_HTML,
    FIELD_CONTENT_TEXT,
)
from app.utils.sanitize import sanitize_html


def prepare_post_content(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Подготавливает поля контента перед сохранением/обновлением."""
    result = dict(fields)
    if FIELD_CONTENT_HTML in result:
        cleaned_html = sanitize_html(result[FIELD_CONTENT_HTML] or '')
        result[FIELD_CONTENT_HTML] = cleaned_html
        result[FIELD_CONTENT_TEXT] = (cleaned_html or '')[
            :CONTENT_TEXT_MAX_LENGTH
        ]
    return result
