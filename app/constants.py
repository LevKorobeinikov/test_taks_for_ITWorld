TOKEN_TYPE_BEARER = 'bearer'
LIMIT = 100
OFFSET = 0

# Ошибки/сообщения для auth/token
ERR_USER_ALREADY_EXISTS = 'Пользователь с таким email уже существует'
ERR_INVALID_TOKEN_TYPE = 'Неверный тип токена'
ERR_TOKEN_REVOKED_OR_NOT_FOUND = 'Токен отозван или не найден'
ERR_FAILED_TO_CREATE_TOKENS = 'Не удалось создать токены'
ERR_INVALID_CREDENTIALS = 'Неверные учетные данные'
ERR_MISSING_REFRESH_TOKEN = 'Отсутствует параметр refresh_token'
ERR_INVALID_TOKEN = 'Неверный токен'

# Общие ошибки/сообщения для categories
ERR_CATEGORY_NOT_FOUND = 'Категория не найдена'
ERR_CATEGORY_SLUG_EXISTS = 'Категория с таким slug уже существует'

# Общие ошибки/сообщения для posts
ERR_POST_NOT_FOUND = 'Пост не найден'

# Общие ошибки/сообщения для users
ERR_INVALID_TOKEN = 'Неверный токен'
ERR_USER_NOT_FOUND = 'Пользователь не найден'

# Теги роутеров
TAG_AUTH = 'auth'
TAG_USERS = 'users'
TAG_POSTS = 'posts'
TAG_CATEGORIES = 'categories'

# Префиксы роутеров
API_PREFIX = '/api/v1'
AUTH_PREFIX = '/auth'
USERS_PREFIX = '/users'
POSTS_PREFIX = '/posts'
CATEGORIES_PREFIX = '/categories'

# CRUD
USER_ID = 'user_id'

# models
MAX_LENGHT_NAME = 100
MAX_LENGHT_SLUG = 150
MAX_LENGHT_TITLE = 300
MAX_LENGHT_SLUG_POST = 350
MAX_LENGHT_JTI = 128
MAX_LENGHT_EMAIL = 254
MIN_LENGHT_PASSWORD = 8
MIN_LENGHT = 1
SET_NULL = 'SET NULL'
CASCADE = 'CASCADE'

# JWT
CLAIM_SUB = 'sub'
CLAIM_TYPE = 'type'
CLAIM_JTI = 'jti'
CLAIM_IAT = 'iat'
CLAIM_EXP = 'exp'

# JWT типы токен
TOKEN_TYPE_ACCESS = 'access'
TOKEN_TYPE_REFRESH = 'refresh'
REFRESH_ISSUED_AT = 'issued_at'
REFRESH_EXPIRES_AT = 'expires_at'

# Post sanitize
FIELD_CONTENT_HTML = 'content_html'
FIELD_CONTENT_TEXT = 'content_text'
CONTENT_TEXT_MAX_LENGTH = 400
ALLOWED_ATTRS = {'a': ['href', 'title', 'alt']}
ALLOWED_TAGS = [
    'p',
    'br',
    'strong',
    'em',
    'ul',
    'ol',
    'li',
    'a',
    'h1',
    'h2',
    'h3',
    'h4',
    'blockquote',
    'code',
    'pre',
]

ERR_PERMISSION_DENIED = 'Доступ запрещён'
ROLE_ADMIN = 'ADMIN'
ROLE_USER = 'USER'
