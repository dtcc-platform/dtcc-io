#include "dtcc_model/PolygonMethods.h"
#include "dtcc_model/VectorMethods.h"

TEST_CASE("Polygons")
{
    std::vector<Vector2D> pts;
    pts.push_back(Vertex(1,1));
    pts.push_back(Vertex(2,1));
    pts.push_back(Vertex(1,2));
    pts.push_back(Vertex(1,1));

    SECTION("Create polygon")
    {
      Polygon p = CreatePolygon(pts);
      REQUIRE(p.shell().vertices_size()==4);
    }

    SECTION("Create donut")
    {
      std::vector<Vector2D> shell_pts;
      shell_pts.push_back(Vertex(0,0));
      shell_pts.push_back(Vertex(10,0));
      shell_pts.push_back(Vertex(10,10));
      shell_pts.push_back(Vertex(0,10));
      shell_pts.push_back(Vertex(0,0));

      std::vector<LinearRing> holes;

      std::vector<Vector2D> hole1;
      hole1.push_back(Vertex(1,1));
      hole1.push_back(Vertex(2,1));
      hole1.push_back(Vertex(2,2));
      hole1.push_back(Vertex(1,2));
      hole1.push_back(Vertex(1,1));
      holes.push_back(CreateLinearRing(hole1));

      std::vector<Vector2D> hole2;
      hole2.push_back(Vertex(3,3));
      hole2.push_back(Vertex(4,3));
      hole2.push_back(Vertex(4,4));
      hole2.push_back(Vertex(3,4));
      hole2.push_back(Vertex(3,3));
      holes.push_back(CreateLinearRing(hole2));

      auto p = CreatePolygon(shell_pts,holes);
      REQUIRE(p.shell().vertices_size()==5);
      REQUIRE(p.holes_size()==2);
      REQUIRE(p.holes(1).vertices(0).x()==3);

    }

    SECTION("Create donut2")
    {
      std::vector<Vector2D> shell_pts;
      shell_pts.push_back(Vertex(0,0));
      shell_pts.push_back(Vertex(10,0));
      shell_pts.push_back(Vertex(10,10));
      shell_pts.push_back(Vertex(0,10));
      shell_pts.push_back(Vertex(0,0));

      std::vector<std::vector<Vector2D>> holes;

      std::vector<Vector2D> hole1;
      hole1.push_back(Vertex(1,1));
      hole1.push_back(Vertex(2,1));
      hole1.push_back(Vertex(2,2));
      hole1.push_back(Vertex(1,2));
      hole1.push_back(Vertex(1,1));
      holes.push_back(hole1);

      std::vector<Vector2D> hole2;
      hole2.push_back(Vertex(3,3));
      hole2.push_back(Vertex(4,3));
      hole2.push_back(Vertex(4,4));
      hole2.push_back(Vertex(3,4));
      hole2.push_back(Vertex(3,3));
      holes.push_back(hole2);

      auto p = CreatePolygon(shell_pts,holes);
      REQUIRE(p.shell().vertices_size()==5);
      REQUIRE(p.holes_size()==2);
      REQUIRE(p.holes(1).vertices(0).x()==3);

    }

    SECTION("Offset polygon")
    {
      Polygon p = CreatePolygon(pts);
      Vector2D o = Vertex(2,3);
      OffsetPolygon(p,o);
      auto shell_verts = p.shell().vertices();
      REQUIRE(shell_verts[0].x()==3);
      REQUIRE(shell_verts[0].y()==4);
      REQUIRE(shell_verts[2].x()==3);
      REQUIRE(shell_verts[2].y()==5);
    }




}
