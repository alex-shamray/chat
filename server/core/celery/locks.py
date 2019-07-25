"""
Celery task locking utilities.

Based partially on an example in the Task Cookbook [1].

[1] http://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time

Example Usage::

    >>> from core.celery.locks import cache_lock
    >>> @task(bind=True)
    >>> def import_feed(self, feed_url):
    ...     # The cache key consists of the task name and the MD5 digest
    ...     # of the feed URL.
    ...     feed_url_hexdigest = md5(feed_url).hexdigest()
    ...     lock_id = '{0}-lock-{1}'.format(self.name, feed_url_hexdigest)
    ...     logger.debug('Importing feed: %s', feed_url)
    ...     with cache_lock(lock_id, self.app.oid) as acquired:
    ...         if acquired:
    ...             return Feed.objects.import_feed(feed_url).url
    ...     logger.debug(
    ...         'Feed %s is already being imported by another worker', feed_url)
"""
from contextlib import contextmanager

from celery.five import monotonic
from django.core.cache import cache

LOCK_EXPIRE = 60 * 2  # Lock expires in 2 minutes


@contextmanager
def cache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)
