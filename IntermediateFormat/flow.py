import IntermediateFormat.objects as objects
from typing import List


def flowResolver(blocks: List[objects.SequenceBlock]) -> List[objects.SequenceBlock]:
    inWireToBlock = {}
    for block in blocks:
        inWireToBlock[block.inputWire] = block

    sortedBlocks = []
    currBlock = inWireToBlock[None]  # starting block has in=None
    while currBlock.outputWire != None:
        sortedBlocks.append(currBlock)
        currBlock = inWireToBlock[currBlock.outputWire]
    return sortedBlocks
