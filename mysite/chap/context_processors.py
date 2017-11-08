from .models import Interview
def interview_processor(request):
    interviews = Interview.objects.all()
    return {'interviews':interviews}