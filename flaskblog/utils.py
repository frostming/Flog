import hashlib
import hmac
import time
from collections import OrderedDict
from urllib.parse import urlencode

from flask import current_app, request
from sqlalchemy import func
from typing import Iterable

from .models import Post, Tag


def get_tag_cloud() -> Iterable[Tag]:
    """Get tags order by its heat to generate a tag cloud"""
    tags = Tag.query.join(Tag.posts).with_entities(Tag, func.count(Post.id))\
                                    .group_by(Tag.id)\
                                    .order_by(func.count(Post.id).desc())
    return tags.all()
