from mindpile.Mapping.utils import MethodCall

@MethodCall(target="CommentBlock.vix")
def comment():
    # Python AST doesn't support inserting comments
    return '''
    '''
