# app/context_processors.py

from .models import Tutor, StudentTutorRequest

def pending_requests_processor(request):
    if request.user.is_authenticated and hasattr(request.user, 'tutor'):
        tutor = request.user.tutor
        pending_requests = StudentTutorRequest.objects.filter(tutor=tutor, status='pending')
        has_pending_requests = pending_requests.exists()
    else:
        has_pending_requests = False

    return {'has_pending_requests': has_pending_requests}
