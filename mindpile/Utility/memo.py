import functools

def memoise(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from mindpile.Mapping.utils import global_runs_count
        if wrapper.hasResult != global_runs_count:
            wrapper.result = func(*args, **kwargs)
            wrapper.hasResult = global_runs_count
        return wrapper.result
    wrapper.result = None
    wrapper.hasResult = -1

    return wrapper
