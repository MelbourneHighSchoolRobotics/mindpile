NAMESPACE = "{http://www.ni.com/VirtualInstrument.xsd}"


def addNameSpace(string):
    return NAMESPACE + string


def removeNameSpace(string):
    return "".join(string.split("}")[1::])


def getDepthInfoTree(elem, depth=0):
    return (depth, elem, [getDepthInfoTree(child, depth=depth + 1) for child in elem])


def addSpacing(spaces, text):
    return "\n".join([(" " * spaces) + text for text in text.split("\n")])

