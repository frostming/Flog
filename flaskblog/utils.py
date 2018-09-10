import hashlib
import hmac
import time
from collections import OrderedDict
from urllib.parse import urlencode

from flask import current_app, request
from sqlalchemy import func

from .models import Post, Tag


def get_tag_cloud():
    """Get tags order by its heat to generate a tag cloud"""
    tags = Tag.query.join(Tag.posts).with_entities(Tag, func.count(Post.id))\
                                    .group_by(Tag.id)\
                                    .order_by(func.count(Post.id).desc())
    return tags.all()


def calc_token():
    """Get the upload authorization head with additional params for Tencent qcloud
    See https://cloud.tencent.com/document/product/436/7778
    """
    def sorted_keys(dict_):
        """Sorted lowercase keys joined with ';'"""
        keys = [key.lower() for key in dict_]
        return ';'.join(sorted(keys))

    def dict_to_string(dict_):
        """Return encoded key-value pairs joined with '&'"""
        sorted_dict = OrderedDict((key.lower(), dict_.get(key, ''))
                                  for key in sorted(dict_.keys()))
        return urlencode(sorted_dict)

    method = request.args.get('method', 'get').lower()
    path = request.args.get('path', '/')
    query_params = dict()
    headers = dict()
    if path[0] != '/':
        path = '/' + path
    secret_id = current_app.config['COS_SECRET_ID']
    secret_key = current_app.config['COS_SECRET_KEY']
    now = int(time.time())
    expired = now + 600

    q_algorithm = 'sha1'
    q_ak = secret_id
    q_key_time = q_sign_time = '{};{}'.format(now, expired)
    q_headerlist = sorted_keys(headers)
    q_paramslist = sorted_keys(query_params)

    sign_key = hmac.new(secret_key.encode('utf-8'), q_key_time.encode('utf-8'),
                        digestmod=hashlib.sha1).hexdigest()
    http_string = '\n'.join([
        (method or 'get').lower(),
        path,
        dict_to_string(query_params),
        dict_to_string(headers),
        ''
    ])
    string_to_sign = '\n'.join([
        q_algorithm,
        q_sign_time,
        hashlib.sha1(http_string.encode('utf-8')).hexdigest(),
        ''
    ])

    signature = hmac.new(sign_key.encode('utf-8'),
                         string_to_sign.encode('utf-8'),
                         digestmod=hashlib.sha1).hexdigest()

    authorization = {
        'q-sign-algorithm': q_algorithm,
        'q-ak': q_ak,
        'q-sign-time': q_sign_time,
        'q-key-time': q_key_time,
        'q-header-list': q_headerlist,
        'q-url-param-list': q_paramslist,
        'q-signature': signature
    }

    return '&'.join('{}={}'.format(k, v)
                    for (k, v) in authorization.items())
