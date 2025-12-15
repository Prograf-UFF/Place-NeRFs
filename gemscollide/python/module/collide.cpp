/**

**/

#ifndef __COLLIDE_CPP__
#define __COLLIDE_CPP__

#include "../../cpp/include/gemsiv/collide.cpp"
#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <boost/python/copy_non_const_reference.hpp>
#include <boost/python/return_value_policy.hpp>


namespace py = boost::python;
namespace np = boost::python::numpy;


np::ndarray wrap_mak_box()
{
    static double box_tmp[24];
    mak_box(box_tmp);

    // Turning the output into a numpy array
    np::dtype dt = np::dtype::get_builtin<double>();
    py::tuple shape = py::make_tuple(24); // It has shape (24,)
    py::tuple stride = py::make_tuple(sizeof(double)); // 1D array, so its just size of double
    np::ndarray result = np::from_data(box_tmp, dt, shape, stride, py::object());
    return result;
}


np::ndarray wrap_mak_cyl()
{
    static double cyl_tmp[108];
    mak_cyl(cyl_tmp);

    // Turning the output into a numpy array
    np::dtype dt = np::dtype::get_builtin<double>();
    py::tuple shape = py::make_tuple(108); // It has shape (24,)
    py::tuple stride = py::make_tuple(sizeof(double)); // 1D array, so its just size of double
    np::ndarray result = np::from_data(cyl_tmp, dt, shape, stride, py::object());
    return result;
}


np::ndarray wrap_mak_sph()
{
    static double sph_tmp[1026];
    mak_sph(sph_tmp);

    // Turning the output into a numpy array
    np::dtype dt = np::dtype::get_builtin<double>();
    py::tuple shape = py::make_tuple(1026); // It has shape (,)
    py::tuple stride = py::make_tuple(sizeof(double)); // 1D array, so its just size of double
    np::ndarray result = np::from_data(sph_tmp, dt, shape, stride, py::object());
    return result;
}


py::dict wrap_get_polyhedron2dict(Polyhedron polyhdrn)
{
    py::dict result;
    // Turning the output into numpy array
    np::dtype dt = np::dtype::get_builtin<double>();
    py::tuple shape = py::make_tuple(polyhdrn->m * 3);
    py::tuple stride = py::make_tuple(sizeof(double));
    result["verts"] = np::from_data(polyhdrn->verts, dt, shape, stride, py::object());
    result["m"] = polyhdrn->m;
    result["trn"] = np::from_data(polyhdrn->trn, dt, py::make_tuple(3), stride, py::object());
    return result;
}

Polyhedron wrap_init_polyhedron(np::ndarray const & verts, int m, double tx, double ty, double tz)
{
    Polyhedron Polyhedron1 = (Polyhedron)malloc(sizeof(struct polyhedron));
    init_polyhedron(Polyhedron1, reinterpret_cast<double*>(verts.get_data()), m,  tx, ty, tz);
    return Polyhedron1;
}

np::ndarray wrap_get_trn(Polyhedron polyhdrn)
{
    np::dtype dt = np::dtype::get_builtin<double>();
    py::tuple stride = py::make_tuple(sizeof(double)*1);
    return np::from_data(polyhdrn->trn, dt, py::make_tuple(3), stride, py::object());
}


Couple wrap_init_couple(Polyhedron polyhdrn1, Polyhedron polyhdrn2)
{
    Couple Couple1 = (Couple)malloc(sizeof(struct couple));
    Couple1->polyhdrn1 = polyhdrn1;   Couple1->polyhdrn2 = polyhdrn2;
    Couple1->n = 0;
    Couple1->plane_exists = FALSE;
    return Couple1;
}



BOOST_PYTHON_MODULE(collide)
{
    Py_Initialize();
    np::initialize();

    py::class_<polyhedron>("Polyhedron");
    py::class_<couple>("Couple");

    py::def("mak_box", wrap_mak_box);
    py::def("mak_cyl", wrap_mak_cyl);
    py::def("mak_sph", wrap_mak_sph);

    py::def("init_polyhedron", wrap_init_polyhedron, py::return_value_policy<py::manage_new_object>());
    py::def("init_couple", wrap_init_couple, py::return_value_policy<py::manage_new_object>());
    py::def("get_trn", wrap_get_trn);
    py::def("get_polyhedron2dict", wrap_get_polyhedron2dict);

    py::def("move_polyhedron", move_polyhedron);
    py::def("Collision", Collision);
}

#endif // __COLLIDE_CPP__