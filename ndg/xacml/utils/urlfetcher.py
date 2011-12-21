"""NDG XACML data fetch by URL utility

NERC DataGrid
"""
__author__ = "R B Wilkinson"
__date__ = "03/11/11"
__copyright__ = "(C) 2011 Science and Technology Facilities Council"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
import os
import urllib2
import urlparse

log = logging.getLogger(__name__)

def fetch_stream_from_url(url, debug=False):
    """Returns data retrieved from a URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: data retrieved from URL or None
    @rtype: file derived type
    """
    response = open_url(url, debug)
    return response

def fetch_data_from_url(url, debug=False):
    """Returns data retrieved from a URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: data retrieved from URL or None
    @rtype: str
    """
    response = open_url(url, debug)
    return_data = response.read()
    response.close()
    return return_data

def open_url(url, debug=False):
    """Attempts to open a connection to a specified URL.
    @param url: URL to attempt to open
    @type: str
    @param debug: debug flag for urllib2
    @type: bool
    @return: tuple (
    @rtype: tuple (
        int: returned HTTP status code or 0 if an error occurred
        str: returned message or error description
        file-like: response object
    )
    """
    debuglevel = 1 if debug else 0

    # Set up handlers for URL opener.
    http_handler = urllib2.HTTPHandler(debuglevel=debuglevel)

    handlers = [http_handler]

    # Explicitly remove proxy handling if the host is one listed in the value of
    # the no_proxy environment variable because urllib2 does use proxy settings
    # set via http_proxy and https_proxy, but does not take the no_proxy value
    # into account.
    if not _should_use_proxy(url):
        handlers.append(urllib2.ProxyHandler({}))
        log.debug("Not using proxy")

    opener = urllib2.build_opener(*handlers)

    # Open the URL and check the response.
    try:
        response = opener.open(url)
    except urllib2.HTTPError, exc:
        # Re-raise as simple exception
        raise Exception(exc.__str__())
    return response

def _should_use_proxy(url):
    """Determines whether a proxy should be used to open a connection to the
    specified URL, based on the value of the no_proxy environment variable.
    @param url: URL
    @type: str
    @return: flag indicating whether proxy should be used
    @rtype: bool
    """
    no_proxy   = os.environ.get('no_proxy', '')

    urlObj = urlparse.urlparse(url)
    for np in [h.strip() for h in no_proxy.split(',')]:
        if urlObj.hostname == np:
            return False

    return True
