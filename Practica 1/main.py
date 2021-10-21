from Image import *

if __name__ == "__main__":
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

    agent1 = Agent("A2", TypeAgent.humano, InitalCords=(2, 'B'), stageText=readFile("lab1.txt"),
                   FinalCords=(3, 'B'))
    agent1.printAgent()
    print(f"Costo snow {agent1.returnCost(typeTerrain=Terrain.Snow)}")
