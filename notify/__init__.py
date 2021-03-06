from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from future import standard_library
standard_library.install_aliases()

# Version numbering follows Semantic Versionning:
#
# Given a version number MAJOR.MINOR.PATCH, increment the:
# - MAJOR version when you make incompatible API changes,
# - MINOR version when you add functionality in a backwards-compatible manner, and
# - PATCH version when you make backwards-compatible bug fixes.
#
# -- http://semver.org/

__version__ = '5.3.0'

from notify.errors import REQUEST_ERROR_STATUS_CODE, REQUEST_ERROR_MESSAGE  # noqa

from notify.notifications import NotificationsAPIClient as Client # noqa
from notify.utils import prepare_upload # noqa
