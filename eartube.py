# eartube
from build123d import *
from ocp_vscode import *

outd= 4
idc= 3.5
cirr=2.32
with BuildPart() as part:
    # Define the spine/path — an arc connecting the two circle centers
    with BuildLine() as path:
       
        Line((0,0, 0), (38, 0, 0))  # straight line extension
        Line((38, 0, 0),(80, 8, 0))
        Line((80, 8, 0),(148, 30, 0))
        RadiusArc((148, 30, 0), (168, 66, 0), radius=-29)  # curved path
    # Profile to sweep (circle)
    with BuildSketch(Plane(origin=(0,0,0), z_dir=path.wires()[0] % 0)):
         Ellipse(idc,outd)  # circle profile centered on the path   
    sweep(path=path.wires()[0])


#inner cut
    with BuildLine() as path:
        Line((0,0, 0), (38, 0, 0))  # straight line extension
        Line((38, 0, 0),(80, 8, 0))
        Line((80, 8, 0),(148, 30, 0))
        RadiusArc((148, 30, 0), (168, 66, 0), radius=-29)  # curved path
    # Profile to sweep (circle)
    with BuildSketch(Plane(origin=(0,0,0), z_dir=path.wires()[0] % 0)):
         Circle(cirr)  # circle profile centered on the path   
    
    sweep(path=path.wires()[0], mode=Mode.SUBTRACT)  # subtract the smaller tube from the larger one to create a hollow tube

    #cut to set angle
    with BuildSketch(Plane.XY) as sketch:
        with BuildLine():
            Line((164, 62), (172.1,66))
            Line((172.1,66), (172.1, 67))  # horizontal line
            Line((172.1,67), (164, 67))  # diagonal line at 45 degrees
            Line((164, 67), (164, 62))  # vertical line
        make_face()
    extrude(amount=10, both=True, mode=Mode.SUBTRACT)  # extrude in both directions to ensure it fully cuts through the tube
 
 
 #small cy on face after cuve
    face5 = part.faces()[8]
    with BuildSketch(face5):
        Circle(4.5/2)   # 20mm diameter = 10mm radius
    extrude(amount=2)

#big circle on small cy.
    with BuildSketch(face5.offset(2)):
        Circle(4)   # 20mm diameter = 10mm radius
    extrude(amount=1.5)
    #cut 
    with BuildSketch(face5):
        Circle(2.4/2)   # 20mm diameter = 10mm radius
    extrude(amount=4, mode=Mode.SUBTRACT)  # cut a hole in the cylinder



# mould filler in bottom
#lower side rect
    with BuildSketch(Plane.XY.offset(-idc)):
        with Locations((2,0)):
            Rectangle(8, 2)
    extrude(amount=.2)

### mold filler 
    t=-2
    with BuildSketch(Plane.XY.offset(-idc)):
        # with Locations((1,0)):
        with BuildLine():
                RadiusArc((t, -5), (t, 5), 5)   # curved arc
                Line((t, -5), (t, 5))          # closing line
        make_face()  
    extrude(amount=.5)




#loft operation
    with BuildSketch(Plane.YZ):   # YZ plane at x=0
        Ellipse(outd, idc)         # major=4, minor=3.5
    
    # Inner circle profile — same plane (they meet at same face)
    with BuildSketch(Plane.YZ.offset(1)):  # offset creates depth of funnel
        Circle(cirr)                  # inner tube radius
    
    extrude(amount=1, mode=Mode.SUBTRACT)  # cut a funnel-shaped hole into the end of the tube

    with BuildSketch(Plane.YZ):   # YZ plane at x=0
              Circle(cirr)            # major=4, minor=3.5
    
    # Inner circle profile — same plane (they meet at same face)
    with BuildSketch(Plane.YZ.offset(1)):  # offset creates depth of funnel
             Ellipse(outd, idc)    # inner tube radius
    
    loft()

#inner cut after loft
    with BuildSketch(Plane.YZ.offset(0)):  # offset creates depth of funnel
        Circle(cirr)                  # inner tube radius
    
    extrude(amount=1, mode=Mode.SUBTRACT)

    #rectangle of bottom filler fixing
    with BuildSketch(Plane.XY.offset(-idc)):
        with Locations((2,0)):
            Rectangle(8, 2)
    extrude(amount=.2)


#mold filler in upper
    face25 = part.faces()[21] # 16
    with BuildSketch(face25):
        with Locations((0,3.9)):
            Rectangle(2,0.2)      
    extrude(amount=2.5)

    face2 = part.faces()[2]
    with BuildSketch(face2):
        with Locations((0,-1.25)):
            with BuildLine():
                RadiusArc((5, -1.25), (-5, -1.25), 5)   # curved arc
                Line((5, -1.25), (-5, -1.25))          # closing line
            make_face()
    extrude(amount=-0.5)


show(part)

vol = part.part.volume

print(f"Volume = {vol:.2f} mm³")
export_stl(part.part , "/Users/softage/Downloads/Stethoscope/eartube.stl")