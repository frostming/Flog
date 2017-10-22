from .models import Post, Tag
from sqlalchemy import func


def get_tag_cloud():
    """Get tags order by its heat to generate a tag cloud"""
    tags = Tag.query.join(Tag.posts).with_entities(Tag, func.count(Post.id))\
                                    .group_by(Tag.id)\
                                    .order_by(func.count(Post.id).desc())
    return tags.all()
