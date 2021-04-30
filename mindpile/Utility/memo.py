import functools

def memoise(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.hasResult:
            wrapper.result = func(*args, **kwargs)
            wrapper.hasResult = True
        return wrapper.result
    wrapper.result = None
    wrapper.hasResult = False

    return wrapper
