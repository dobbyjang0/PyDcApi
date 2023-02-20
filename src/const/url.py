HTTPS_DC_URL = 'https://m.dcinside.com'
DC_URL = 'm.dcinside.com'
UPLOAD_HOST_URL = "mupload.dcinside.com"

# ajax 관련
COMMENT_WRITE_AJAX = "https://m.dcinside.com/ajax/comment-write"
ACCESS_AJAX = "https://m.dcinside.com/ajax/access"
WRITE_FILTER_AJAX = "https://m.dcinside.com/ajax/w_filter"
IMAGE_FILTER_AJAX = "https://m.dcinside.com/ajax/i_filter"

WRITE_PHP = "https://mupload.dcinside.com/write_new.php"
UPLOAD_IMG_PHP = "https://mupload.dcinside.com/upload_img.php"

# 로그인 관련
LOGIN_ACCESS_URL = "https://msign.dcinside.com/login/access"
LOGIN_URL = "https://msign.dcinside.com/login"


def DOCUMENT_VIEW_URL(board_id, document_id):
    return f'https://m.dcinside.com/board/{board_id}/{document_id}'


def DOCUMENT_WRITE_URL(board_id):
    return f'https://m.dcinside.com/write/{board_id}'
