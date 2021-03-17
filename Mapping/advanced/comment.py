from Mapping.types import InPort, OutPort, List
from Mapping.utils import MethodCall, Requires, Setup

@MethodCall(target="CommentBlock.vix")
def comment():
    # Python AST doesn't support inserting comments
    return '''
    '''
