from Image import *


if __name__ == "__main__":
    # stage2 = Stage(readFile("lab2.txt"))
    # stage2.stageToImage([
    #    [128, 128, 128],
    #    [250, 191, 143],
    #    [0, 175, 255],
    #    [255, 192, 0],
    #    [150, 210, 80]
    # ], 'lab2')

    # stage2.addCellsHide(1, 'A')
    # print(stage2.cellsHide)
    # stage2.addCellsHide(1, 'A')
    # print(stage2.cellsHide)
    # stage2.addCellsHide(1, 'B')
    # print(stage2.cellsHide)
    # stage2.textToImage(0,0,"a","lab1.png")
    # stage2.textToImage(0,1,"b","lab1.png")
    # stage1.textToImage(0, 2, "c", "lab2.png")
    # stage1.textToImage(0, 2, "b", "lab2.png")

    agent1 = Agent("A2", TypeAgent.humano, InitalCords=giveCords((2, 'A')), stageText=readFile("lab1.txt"), FinalCords=giveCords((2, 'A')))
    agent1.printAgent()
    print(f"Costo snow {agent1.returnCost(typeTerrain=Terrain.Snow)}")