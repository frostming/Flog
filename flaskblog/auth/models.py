from ..models import db


class OAuth2Token(db.Model):
    name = db.Column(db.String(40))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(200))
    refresh_token = db.Column(db.String(200))
    expires_at = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("tokens", lazy="dynamic"))

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )
