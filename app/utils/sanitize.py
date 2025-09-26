import bleach

from app.constants import ALLOWED_ATTRS, ALLOWED_TAGS


def sanitize_html(raw_html: str) -> str:
    return bleach.clean(
        raw_html or '',
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )
