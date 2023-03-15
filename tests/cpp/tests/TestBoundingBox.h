#include "dtcc_model/BoundingBoxMethods.h"

TEST_CASE("BoundingBox")
{
    SECTION("2D vector bounds")
    {
        std::vector<Vector2D> vecs;

        Vector2D v1;
        v1.set_x(1.0);
        v1.set_y(2.0);
        vecs.push_back(v1);

        Vector2D v2;
        v2.set_x(6.0);
        v2.set_y(2.0);
        vecs.push_back(v2);

        Vector2D v3;
        v3.set_x(5.0);
        v3.set_y(7.0);
        vecs.push_back(v3);

        Vector2D v4;
        v4.set_x(-1.0);
        v4.set_y(1.0);
        vecs.push_back(v4);


        auto bb = VectorBoundingBox(vecs);
        auto bb_P = bb.p();
        auto bb_Q = bb.q();
        REQUIRE(bb_P.x() == -1.0);
        REQUIRE(bb_P.y() == 1.0);
        REQUIRE(bb_Q.x() == 6.0);
        REQUIRE(bb_Q.y() == 7.0);
    }

    SECTION("Union")
    {
      BoundingBox2D bb1 = BoundingBox(0,0,5,5);
      BoundingBox2D bb2 = BoundingBox(2,3,7,8);

      auto unionBox = Union(bb1,bb2);
      auto union_P = unionBox.p();
      auto union_Q = unionBox.q();
      REQUIRE(union_P.x() == 0);
      REQUIRE(union_P.y() == 0);
      REQUIRE(union_Q.x() == 7);
      REQUIRE(union_Q.y() == 8);
    }

    SECTION("Area")
    {
      BoundingBox2D bb = BoundingBox(1,2,3,4);
      REQUIRE(Area(bb)==4);
    }
}
