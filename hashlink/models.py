import mongoengine

HASHLINK_REGEX = r'[A-Za-z0-9]+'

class HashlinkDocument(mongoengine.Document):
    state = mongoengine.DictField(required=True, unique=True)
    hashlink = mongoengine.StringField(required=True, unique=True, regex=HASHLINK_REGEX, min_length=8, max_length=8)

class HashlinkPathDocument(mongoengine.Document):
    previous = mongoengine.StringField(required=False, regex=HASHLINK_REGEX, min_length=8, max_length=8)
    current = mongoengine.StringField(required=True, regex=HASHLINK_REGEX, min_length=8, max_length=8)
    session_id = mongoengine.StringField(required=True)
