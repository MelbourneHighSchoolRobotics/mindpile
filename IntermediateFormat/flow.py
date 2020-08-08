from typing import List


def flowResolver(blocks):
    inWireToBlock = {}
    for block in blocks:
        inWireToBlock[block.inputWire] = block

    sortedBlocks = []
    currBlock = inWireToBlock[None]  # starting block has in=None
    sortedBlocks.append(currBlock)
    while True:
        currBlock = inWireToBlock[currBlock.outputWire]
        sortedBlocks.append(currBlock)
        if currBlock.outputWire == None:
            break
    return sortedBlocks
