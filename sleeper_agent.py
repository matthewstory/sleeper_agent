import sys, traceback
import gc
import collections
import _sleeper_agent_activation

def _sizeof_fmt(num):
    '''Shamelessly taken from StackOverflow:

       http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    '''
    for x in ['b','KB','MB','GB','TB']:
        if num < 1024.0:
            break
        num /= 1024.0
    return "%3.1f %s" % (num, x)

def _get_state_info():
    """Return state of current process, as a string.

    Returns a formatted list of threads known to the Python
    interpreter, together with their stack traces.

    One of the threads will have this function call *appended* to its
    original stack trace. I still don't know how to get rid of that."""
    return "\n\n".join(
        "### Thread {0}:\n{1}".format(
            thread_id, ''.join(traceback.format_stack(frame)))
        for thread_id, frame in sys._current_frames().items() )


def _get_mem_info():
    '''Return memory usage information'''
    obj_map = collections.defaultdict(lambda: { 'count': 0, 'size': 0})
    for obj in gc.get_objects():
        obj_map[type(obj)]['count'] += 1
        obj_map[type(obj)]['size'] += sys.getsizeof(obj)

    return "\n".join(
        "{size:>8} {count:>8} object{s} {type_:>50}".format(type_=type_, count=val['count'],
                                                            s='' if val['count'] == 1 else 's',
                                                            size=_sizeof_fmt(val['size']))
        for type_, val in sorted(obj_map.iteritems(), key=lambda v: -v[1]['size']))
