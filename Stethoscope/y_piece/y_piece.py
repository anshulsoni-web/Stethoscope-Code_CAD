
from build123d import *
from ocp_vscode import show
import math

# Parameters
pipe_radius = 4.3
pipe_radius2 = 3
wall        = 1.25
main_length = 35
branch_length = 23
half_angle  = 20        # 20° each side = 40° total between branches

# Compute branch axis directions from rotation (0, ±half_angle, 0)
# Z = (0,0,1) rotated by ±half_angle around Y → (±sin, 0, cos)
a = math.radians(half_angle)
b1_dir = Vector(-math.sin(a), 0, math.cos(a))  # axis of branch 1 (ry = -20°)
b2_dir = Vector( math.sin(a), 0, math.cos(a))  # axis of branch 2 (ry = +20°)

#varying the angle for making semicircle on small pipe. 
aa = math.radians(half_angle+90)
bb1_dir = Vector(-math.sin(aa), 0, math.cos(aa))  # axis of branch 1 (ry = -20°)
bb2_dir = Vector( math.sin(aa), 0, math.cos(aa))  # axis of branch 2 (ry = +20°)


# Planes for loft profiles
plane_top = Plane(origin=(0,  0,   main_length),      z_dir=(0, 0, 1))
plane_b1  = Plane(origin=(-5, 1.3, main_length + 14), z_dir=b1_dir)
plane_b2  = Plane(origin=( 5, 1.3, main_length + 14), z_dir=b2_dir)

with BuildPart() as y_pipe:


    # Main pipe — along Z axis
    Cylinder(radius=pipe_radius,        height=main_length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    Cylinder(radius=pipe_radius - wall, height=main_length, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Branch pipe 1 — rotated +20° around Y axis
    with Locations(Location((-5, 1.3, 35+14), (0, -half_angle, 0))):
        Cylinder(radius=pipe_radius2,        height=branch_length, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=pipe_radius2 - wall, height=branch_length, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Branch pipe 2 — rotated -20° around Y axis
    with Locations(Location((5, 1.3, 35+14), (0, half_angle, 0))):
        Cylinder(radius=pipe_radius2,        height=branch_length, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=pipe_radius2 - wall, height=branch_length, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Loft junction: main pipe top → branch 1 bottom (outer wall)
    with BuildSketch(plane_top): Circle(pipe_radius)
    with BuildSketch(plane_b1):  Circle(pipe_radius2)
    loft()

    # Loft junction: main pipe top → branch 2 bottom (outer wall)
    with BuildSketch(plane_top): Circle(pipe_radius)
    with BuildSketch(plane_b2):  Circle(pipe_radius2)
    loft()

    # Loft junction: main pipe top → branch 1 bottom (hollow interior — subtract)
    with BuildSketch(plane_top): Circle(pipe_radius - wall)
    with BuildSketch(plane_b1):  Circle(pipe_radius2 - wall)
    loft(mode=Mode.SUBTRACT)

    # Loft junction: main pipe top → branch 2 bottom (hollow interior — subtract)
    with BuildSketch(plane_top): Circle(pipe_radius - wall)
    with BuildSketch(plane_b2):  Circle(pipe_radius2 - wall)
    loft(mode=Mode.SUBTRACT)

# big pipe semicircle at the begining of big pipe
    dist = -0.5
    width=2
    height=3.5
    some_depth=-0.5
    with BuildSketch(Plane.XZ.offset(-pipe_radius)):
        with Locations((0, 0.5)):
            with BuildLine():
                RadiusArc((-5, dist), (5, dist), -5)   # curved arc
                Line((5, dist), (-5, dist))             # closing line
        make_face()                                 # ← outside BuildLine, inside BuildSketch
        with Locations((0, 1.25)):
            Rectangle(2, 3.5)
    extrude(amount=0.5/2, both=True)                      # extrude in both directions to intersect pipe



# # fillet on end of secondary cylinders 46 and 35 are edge ids
    fillet(y_pipe.edges()[46], radius=1.2499)
    fillet(y_pipe.edges()[35], radius=1.2499)

#semicircle at the end of small cylinders
# At end of branch 1
    end_b1 = plane_b1.origin + b1_dir * branch_length
    with BuildSketch(Plane(origin=end_b1, z_dir=(0, 1, 0), x_dir=(-bb1_dir)).offset(pipe_radius2)):
        Rectangle(width, height)
        with BuildLine():
            RadiusArc((-5, dist), (5, dist), -5)   # curved arc
            Line((5, dist), (-5, dist))             # closing line
        make_face()

    extrude(amount=some_depth)

# At end of branch 2
    end_b2 = plane_b2.origin + b2_dir * branch_length
    with BuildSketch(Plane(origin=end_b2, z_dir=(0, 1, 0), x_dir=(bb2_dir)).offset(pipe_radius2)):
        with Locations((0,1.25)):
            Rectangle(width, height)
       
        with BuildLine():
            RadiusArc((-5, dist), (5, dist), -5)   # curved arc
            Line((5, dist), (-5, dist))             # closing line
        make_face()
    extrude(amount=some_depth)


show(y_pipe)

vol = y_pipe.part.volume

print(f"Volume = {vol:.2f} mm³")  

export_stl(y_pipe.part , "/Users/softage/Downloads/Stethoscope/y_piece.stl")