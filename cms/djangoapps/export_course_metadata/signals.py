"""
This file exports metadata about the course.
Initially the export goes to S3,
but the storage class could be used for other backends in the future.

This data is initially being used by Braze Connected Content to include
section highlights in emails, but may be used for other things in the future.
"""

import json
import logging

from django.core.files.base import ContentFile
from django.dispatch import receiver
from openedx.core.djangoapps.schedules.content_highlights import get_all_course_highlights
from xmodule.modulestore.django import SignalHandler

from .storage import course_metadata_export_storage
from .toggles import EXPORT_COURSE_METADATA_FLAG

log = logging.getLogger(__name__)


@receiver(SignalHandler.course_published)
def export_course_metadata(sender, course_key, **kwargs):  # pylint: disable=unused-argument
    """
    Export course metadata on course publish.

    File format
    '{"highlights": [["week1highlight1", "week1highlight2"], ["week1highlight1", "week1highlight2"], [], []]}'
    To retrieve highlights for week1, you would need to convert to json, then do
    course_metadata['highlights'][0]

    This data is initially being used by Braze Connected Content to include
    section highlights in emails, but may be used for other things in the future.
    """
    if EXPORT_COURSE_METADATA_FLAG.is_enabled():
        highlights = get_all_course_highlights(course_key)
        highlights_content = ContentFile(json.dumps({"highlights": highlights}))
        course_metadata_export_storage.save('course_metadata_export/{}'.format(course_key), highlights_content)
