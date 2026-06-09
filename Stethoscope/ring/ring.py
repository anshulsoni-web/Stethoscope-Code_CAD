from build123d import *
from ocp_vscode import show

with BuildPart() as con:  # Missing parentheses ()
    # with BuildSketch as fourth:
    Cone(
    bottom_radius=45/2,   # half of 100mm bottom diameter
    top_radius=41.5/2,      # half of 40mm top diameter
    height=6
    )
    # align=(Align.CENTER, Align.CENTER, Align.MIN)  # sits on top of plane
    # Cone(
    #     bottom_radius=50-2,   # half of 100mm bottom diameter
    #     top_radius=20-2,      # half of 40mm top diameter
    #     height=80,
    #     mode= Mode.SUBTRACT
    # )
    with BuildSketch():
        Circle(36/2)
    extrude(amount=-3, mode=Mode.SUBTRACT)
    with BuildSketch():
        Circle(36/2)
    extrude(amount=3, mode= Mode.SUBTRACT)
    with BuildSketch():
        Circle(40/2)
    extrude(amount=-2.5, mode= Mode.SUBTRACT)
    with BuildSketch():
        Circle(40/2)
    extrude(amount=3, mode= Mode.SUBTRACT)
show(con)  # Pass the object to show()


vol = con.part.volume

print(f"Volume = {vol:.2f} mm³")

export_stl(con.part , "/Users/softage/Downloads/Stethoscope/ring.stl")