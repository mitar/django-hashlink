from django import http
from django.core import signing
from django.utils import crypto, simplejson

from . import models

SESSION_ID_SALT = 'django-hashlink'

def hashlink_view(request):
    def store_path(previous, hashlink):
        if previous != hashlink:
            session_id = signing.base64_hmac(SESSION_ID_SALT, str(request.user.id or request.session.session_key), None)
            models.HashlinkPathDocument.objects.create(previous=previous, current=hashlink, session_id=session_id)
        else:
            # TODO: Log, redundant
            pass

    if not request.method == 'POST':
        # TODO: Log
        return http.HttpResponseBadRequest()

    previous = request.POST.get('previous') or None
    if previous and not models.HashlinkDocument.objects.filter(hashlink=previous).count():
        # TODO: Log
        return http.HttpResponseBadRequest()

    if 'state' in request.POST:
        try:
            state = simplejson.loads(request.POST['state'])
        except ValueError:
            # TODO: Log
            return http.HttpResponseBadRequest()

        if not state:
            # TODO: Log
            return http.HttpResponseBadRequest()

        # TODO: Remove race condition
        try:
            hashlink = models.HashlinkDocument.objects.only('hashlink').get(state=state)
        except models.HashlinkDocument.DoesNotExist:
            # TODO: Improve with database retry if non-unique
            hashlink = models.HashlinkDocument.objects.create(state=state, hashlink=crypto.get_random_string(8))

        store_path(previous, hashlink.hashlink)

        return http.HttpResponse(simplejson.dumps({
            'hashlink': hashlink.hashlink,
        }), mimetype="application/json; charset=utf-8")

    elif 'hashlink' in request.POST:
        try:
            hashlink = models.HashlinkDocument.objects.get(hashlink=request.POST['hashlink'])
        except models.HashlinkDocument.DoesNotExist:
            # TODO: Log
            return http.HttpResponseBadRequest()

        store_path(previous, hashlink.hashlink)

        return http.HttpResponse(simplejson.dumps(hashlink.state), mimetype="application/json; charset=utf-8")

    else:
        # TODO: Log
        return http.HttpResponseBadRequest()
