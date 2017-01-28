default_app_config = 'xcomments.apps.XcommentsConfig'

def get_model():
    from xcomments.models import XComment
    return XComment

def get_form():
    from xcomments.forms import CommentForm
    return CommentForm
