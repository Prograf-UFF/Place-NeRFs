#include "gemsiv/collide.cpp"


/*** RJR 05/26/93 ***********************************************************
 *
 *   This is the Main Program for the Collision Detection example. This test
 *   program creates the vertices of three polyhedra: a sphere, a box, and a
 *   cylinder. The three polyhedra oscillate back and forth along the x-axis.
 *   A collision test is done after each movement on each pair of polyhedra.
 *   This test program was run on an SGI Onyx/4 and an SGI 4D/80.  A total of
 *   30,000 collision detection tests were performed.  There were 3,160
 *   collisions detected. The dist3d function was called in 14% of the
 *   collision tests.  The average number of iterations in dist3d was 1.7.
 *   The above functions are designed to compute accurate solutions when
 *   the polyhedra are simple and convex.  The functions will work on
 *   concave polyhedra, but the solutions are computed using the convex hulls
 *   of the concave polyhedra.	In this case when the algorithm returns a
 *   disjoint result it is exact, but when it returns an intersection result
 *   it is approximate.
 *
 ****************************************************************************/
int main()
{
   Polyhedron	  Polyhedron3, Polyhedron8;
   Couple	  Couple1;
   double	  xstp1, xstp2, xstp3;
   int		  i, steps;
   long		  hits = 0;

   double py3[15] = {-390.25686373, -117.61163866,   -1.69420715,  135.89484434,
       -189.56341869,    1.64550344, -115.50796319,  169.16084437,
          1.93892162,   72.56489377,  299.2505676 ,   -0.95511524,
        297.3050888 , -161.23635462,   -0.93510268};

   double py8[15] = {463.00060755,  121.83975993,   -0.59808138, -215.09500212,
        163.48748597,    1.40254081,   -5.57522154, -216.27788358,
          1.88845039,  -21.27005756, -270.43128155,   -1.32586277,
       -221.06032633,  201.38191922,   -1.36704705};

   Polyhedron3 = (Polyhedron)malloc(sizeof(struct polyhedron));
   init_polyhedron(Polyhedron3, py3, 5,  -589.51681791, -372.47878493, 1.47602802);

   Polyhedron8 = (Polyhedron)malloc(sizeof(struct polyhedron));
   init_polyhedron(Polyhedron8, py8, 5, -1263.3776217086238, -496.46814738521834, 0.637091651454399);

   Couple1 = (Couple)malloc(sizeof(struct couple));
   Couple1->polyhdrn1 = Polyhedron3;   Couple1->polyhdrn2 = Polyhedron8;
   Couple1->n = 0;
   Couple1->plane_exists = FALSE;

   if (Collision(Couple1))
	  hits++;
   printf("number of hits = %ld\n", hits);
}