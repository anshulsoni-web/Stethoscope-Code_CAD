from build123d import *
from ocp_vscode import show

with BuildPart() as head:
    with BuildSketch() as base:
        Circle(42/2)
    extrude (amount=12.8/2, both=True)

    # with BuildSketch(Plane.XY.offset(12.8/2)) as next:
    with BuildSketch(head.faces().sort_by(Axis.Z)[-1]) as next:
        Circle(40/2)
    extrude(amount= 4.44)
# ring on face outer circle
    with BuildSketch(head.faces().sort_by(Axis.Z)[-1]) as ring:   
        Circle(35.7/2)
    extrude(amount=0.56)
#ring on face inner 
    with BuildSketch(head.faces().sort_by(Axis.Z)[-1]) as ring:   
        Circle(33.4/2)
    extrude(amount=-0.56, mode=Mode.SUBTRACT)
#bottom tail
    with BuildSketch(Plane.XZ) as tail:
        with Locations((0,-2.15)):
            Circle(8.5/2)
    extrude(amount= 42/2+20)
# tail cut
    with BuildSketch(Plane.XZ) as tailct:
        with Locations((0,-2.15)):
            Circle(5.3/2)
    extrude(amount= 42/2+20-5.2, mode= Mode.SUBTRACT)
#through cut
    with BuildSketch() as cut:
        Circle(6.88/2)
    extrude(amount=11, mode=Mode.SUBTRACT)
    #cut on back
    with BuildSketch() as cut:
        Circle(6.88/2)
    extrude(amount=-4.8, mode=Mode.SUBTRACT)
#conical cut in bottom of tail
    # Conical cut on XZ plane with 45mm Y offset
    with Locations(Plane.XZ.offset(41)):
        with Locations((0,-2.15)):
             Cone(
            bottom_radius=5.3/2,
            top_radius=6.5/2,
            height=5.2,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
            mode=Mode.SUBTRACT  # this makes it a cut
        )
#the conical cut on ear side
    with Locations(Plane.XY.offset(12.8/2+4.44)):
        Cone(
        bottom_radius= 6.88/2,
        top_radius=33.4/2,
        height=1.68,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
        mode=Mode.SUBTRACT        
    )
        
#bottom
    # with BuildSketch(Plane.XY.offset(-6.4)):
    #     with Locations((0,-42)):
    #         Circle(5)
    # extrude(amount=0.5)

    dist=-42
    with BuildSketch(Plane.XY.offset(-6.4)):
        # with Locations((0,-42)):
        with BuildLine():
            RadiusArc((-5, dist), (5, dist), -5)   # curved arc from left to right
            Line((5, dist), (-5, dist))             # straight line closing the bottom
        make_face() 
        with Locations((0,-40.75)):
            Rectangle(2,3.5)
    extrude(amount=.5)



show(head)
vol = head.part.volume

print(f"Volume = {vol:.2f} mm³")  

export_stl(head.part , "/Users/softage/Downloads/Stethoscope/head.stl")