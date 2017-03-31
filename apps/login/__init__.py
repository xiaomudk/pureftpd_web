from uliweb.orm import get_model
from uliweb.i18n import ugettext_lazy as _
from uliweb import functions
from uliweb.utils.common import import_attr

def get_hexdigest(algorithm, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    try:
        import hashlib
    except ImportError:
        if algorithm == 'md5':
            import md5
            return md5.new(raw_password).hexdigest()
        elif algorithm == 'sha1':
            import sha
            return sha.new(raw_password).hexdigest()
    else:
        if algorithm == 'md5':
            return hashlib.md5(raw_password).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def _get_auth_key():
    from uliweb import settings

    return settings.AUTH.AUTH_KEY

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """

    if enc_password == raw_password:
        return True
    else:
        return False

def encrypt_password(raw_password):
    algo = 'sha1'
    hsh = get_hexdigest(algo,  raw_password)
    return hsh

def get_user():
    """
    return user
    """
    from uliweb import request

    session_key = _get_auth_key()
    user_id = request.session.get(session_key)
    if user_id:
        User = get_model('admin')
        return User.get(user_id)


def default_authenticate(username, password):
    User = get_model('admin')
    if isinstance(username, (str, unicode)):
        user = User.get(User.c.Username==username)
    else:
        user = username
    if user:
        if check_password(user.Password,encrypt_password(password)):
            return True, user
        else:
            return False, {'password': _("Password isn't correct!")}
    else:
        return False, {'username': _('"{}" is not existed!').format(username)}


def login(username):
    """
    return user
    """
    from uliweb.utils.date import now
    from uliweb import request

    User = get_model('admin')

    if isinstance(username, (str, unicode)):
        user = User.get(User.c.Username==username)
    else:
        user = username
    request.session[_get_auth_key()] = user.id
    request.user = user
    return True

def logout():
    """
    Remove the authenticated user's ID from the request.
    """
    from uliweb import request

    request.session.delete()
    request.user = None
    return True

def require_login(f=None, next=None):
    from uliweb.utils.common import wraps

    def _login(next=None):
        from uliweb import request, Redirect, url_for

        if not get_user():
            path = functions.request_url()
            Redirect(next or url_for('login', next=path))

    if not f:
        _login(next=next)
        return

    @wraps(f)
    def _f(*args, **kwargs):
        _login(next=next)
        return f(*args, **kwargs)
    return _f