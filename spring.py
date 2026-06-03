
# from build123d import *
# from ocp_vscode import show

# with BuildPart() as spring:
#     dist=-42
#     with BuildSketch(Plane.XY.offset(-6.4)):
#         # with Locations((0,-42)):
#         with BuildLine():
#             RadiusArc((-5, dist), (5, dist), -5)
#             RadiusArc((-5+1, dist), (5-1, dist), -4)  # curved arc from left to right
#             # Line((5, dist), (-5, dist))             # straight line closing the bottom
#         make_face() 
#     extrude(amount=.5)



#     # with BuildSketch(Plane.XY.offset(-6.4)):
#     #     # with Locations((0,-42)):
#     #     with BuildLine():
#     #         RadiusArc((-5, dist), (5, dist), -5)   # curved arc from left to right
#     #         # Line((5, dist), (-5, dist))             # straight line closing the bottom
#     #     make_face() 
#     #     offset(amount=-0.5)
#     # extrude(amount=.5, mode=Mode.SUBTRACT)


# show(spring)


from build123d import *
from matplotlib.pyplot import spring
from ocp_vscode import show

ri= 18
t=3
ro= 21

with BuildPart() as part:
    with BuildSketch() as sketch:
        # Outer ring: 18mm inner diameter = 9mm inner radius, 3mm thickness = 12mm outer radius
        with BuildLine() as profile:
            CenterArc(center=(0, 0), radius=ri,  start_angle=0, arc_size=-180)   # inner arc
            CenterArc(center=(0, 0), radius=ro, start_angle=0, arc_size=-180)   # outer arc
            # close the two ends with straight lines
            Line((ri, 0),  (ro, 0))
            Line((-ri, 0), (-ro, 0))
        make_face()
    
    extrude(amount=10)



    with BuildSketch() as parallalogram:
        width  = 3
        height = 11.8

        offset = 2.25   # how much the top is shifted sideways

        with BuildLine():
            Polyline(
                (ri,             0),
                (ri + width,         0),
                (ri + width + offset, height),
                (ri + offset,        height),
                (ri,             0),   # close
            )
        make_face()

    extrude(amount=10)



#tilted bodies
#1st rectangle
    circ= 16/2
    tilted = Plane(origin=(-19.5,-0.27,5)).rotated((90, 10, 0))
    with BuildSketch(tilted.offset(0)):
        Rectangle(3,10)
    extrude(amount=-32)
    #2nd circle
    with BuildSketch(tilted.offset(-8-12)):
        with Locations((-15/2,0)):
            Circle(circ)
    extrude(amount=-12)



#loft 
    with BuildSketch(tilted.offset(-12)):
        Rectangle(3,10)
   
    with BuildSketch(tilted.offset(-8-12)):
        with Locations((-15/2,0)):
            Circle(circ)
    loft()

#extrude cut to make flat 
    with BuildSketch(Plane.YZ.offset(-19)):
        with Locations((20,-1.5)):
            Rectangle(25,3)
    extrude(amount=-20, mode=Mode.SUBTRACT)#don't forget to cut
    #hole in circle
    with BuildSketch(tilted.offset(-10)):
        with Locations((-15/2,1)):
            Ellipse(4,3.3)
    extrude(amount=-30, mode=Mode.SUBTRACT)


    fillet(part.edges()[22], radius=1)

#circle p[rofile matching]
    # tilted = Plane(origin=(-25,15,6)).rotated((90, 10, -10))
    # with BuildSketch(tilted.offset(0)):
    #     Rectangle(8,10)
    # extrude(amount=-16)

    mirror(about=Plane.YZ)
    # face4 = part.faces().sort_by(Axis.Y)[-1]
    # with BuildSketch(face4.offset(20)):
    #     Circle(5)
    # extrude(amount=10)

    # face3 = part.faces()[3]
    # with BuildSketch(face3):
    #     Rectangle(5, 5)   # change width/height as needed
    # extrude(amount=10)


show(part)


vol = part.part.volume

print(f"Volume = {vol:.2f} mm³")

export_stl(part.part , "/Users/softage/Downloads/Stethoscope/spring.stl")