import datetime
import logging
import time

from exceptions import TimeoutError


LOG = logging.getLogger(__name__)


def wait_for(func, timeout, delay, *args, **kargs):
    """Decorator for waiting for until a function finished running."""

    poll_timeout = timeout
    poll_sleep_retry = delay

    begin_poll = datetime.datetime.now()
    while True:
        try:
            return func(*args, **kargs)
            break
        except Exception as e:
            if (datetime.datetime.now() - begin_poll).seconds > poll_timeout:
                LOG.exception('Time out after %s seconds.' % poll_timeout)
                raise TimeoutError('Timed out after %s seconds. Reason: '
                                   '%s' % (poll_timeout, e))
            else:
                LOG.debug('Sleeping %s seconds before retrying'
                          '' % poll_sleep_retry)
                time.sleep(poll_sleep_retry)
