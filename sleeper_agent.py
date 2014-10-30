import sys, traceback
import gc
import collections
import itertools
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


def _report_lines(obj_map):
    '''Return a report for an object map'''
    return ("{size:>8} {count:>8} object{s} {type_}".format(
                type_=type_, count=val['count'],
                s='' if val['count'] == 1 else 's',
                size=_sizeof_fmt(val['size']))
            for type_, val in sorted(obj_map.iteritems(),
                key=lambda v: -v[1]['size']))

def _get_mem_info():
    '''Return memory usage information'''
    counts_dflt = lambda: { 'count': 0, 'size': 0}
    totals = collections.defaultdict(counts_dflt)
    obj_map = collections.defaultdict(counts_dflt)
    garbage_map = collections.defaultdict(counts_dflt)

    # harvest objects and garbage
    for objs, map_, type_ in ((gc.get_objects(), obj_map, 'objects'),
                              (gc.garbage, garbage_map, 'garbage')):
        for obj in objs:
            map_[type(obj)]['count'] += 1
            totals[type_]['count'] += 1

            size = sys.getsizeof(obj)
            map_[type(obj)]['size'] += size
            totals[type_]['size'] += size

    # build the report
    return "\n".join(itertools.chain(
        ('### Memory Usage',),
        _report_lines(obj_map),
        _report_lines({ 'total': totals['objects'] }),
        ('### Garbage',),
        _report_lines(garbage_map),
        _report_lines({ 'garbage': totals['garbage'] })))
