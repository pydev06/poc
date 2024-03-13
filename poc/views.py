import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def test_logging(request):
    logger.debug('This is a debug message from the test_logging view.')
    return HttpResponse("Log message was sent. Check the console/frontend.")

