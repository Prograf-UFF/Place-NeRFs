from gemscollide import collide

import numpy as np
def test_pyramid():
    hits = 0
    py3 = [-390.25686373, -117.61163866,   -1.69420715,  135.89484434,
        -189.56341869,    1.64550344, -115.50796319,  169.16084437,
        1.93892162,   72.56489377,  299.2505676 ,   -0.95511524,
        297.3050888 , -161.23635462,   -0.93510268]

    py8 = [463.00060755,  121.83975993,   -0.59808138, -215.09500212,
        163.48748597,    1.40254081,   -5.57522154, -216.27788358,
        1.88845039,  -21.27005756, -270.43128155,   -1.32586277,
        -221.06032633,  201.38191922,   -1.36704705]
    
    Polyhedron3 = collide.init_polyhedron(np.array(py3), 5, -589.51681791, -372.47878493, 1.47602802)
    Polyhedron8 = collide.init_polyhedron(np.array(py8), 5, -1263.3776217086238, -496.46814738521834, 0.637091651454399)

    Couple1 = collide.init_couple(Polyhedron3, Polyhedron8)

    if collide.Collision(Couple1): hits+=1
    print(f"number of hits = {hits}")


def main():
    hits = 0

    box = collide.mak_box()
    cyl = collide.mak_cyl()
    sphere = collide.mak_sph()
    
    Polyhedron1 = collide.init_polyhedron(sphere, 342,  0.0, 0.0, 0.0)
    Polyhedron2 = collide.init_polyhedron(box, 8, 50.0, 0.0, 0.0)
    Polyhedron3 = collide.init_polyhedron(cyl, 36, -50.0, 0.0, 0.0)
    
    Couple1 = collide.init_couple(Polyhedron1, Polyhedron2)
    Couple2 = collide.init_couple(Polyhedron1, Polyhedron3)
    Couple3 = collide.init_couple(Polyhedron3, Polyhedron2)
    
    #/** Perform Collision Tests **/
    xstp1 = 1.0	 
    xstp2 = 5.0
    xstp3 = 10.0  
    steps = 10000

    for i in range(steps):
        collide.move_polyhedron(Polyhedron1, xstp1, 0.0, 0.0)
        collide.move_polyhedron(Polyhedron2, xstp2, 0.0, 0.0)
        collide.move_polyhedron(Polyhedron3, xstp3, 0.0, 0.0)

        if collide.Collision(Couple1): hits+=1
        if collide.Collision(Couple2): hits+=1
        if collide.Collision(Couple3):hits+=1

        if abs(collide.get_trn(Polyhedron1)[0]) > 100.0: xstp1 = -xstp1
        if abs(collide.get_trn(Polyhedron2)[0]) > 100.0: xstp2 = -xstp2
        if abs(collide.get_trn(Polyhedron3)[0]) > 100.0: xstp3 = -xstp3
    
    print(f"number of tests = {steps * 3}")
    print(f"number of hits = {hits}")
    

if __name__=="__main__":
    test_pyramid()