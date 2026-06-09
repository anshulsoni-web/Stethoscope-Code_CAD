from build123d import *
from ocp_vscode import show

with BuildPart() as head:
    with BuildSketch() as cir:
        Circle(30)
    extrude(amount=2)
    with BuildSketch() as icir:
        Circle(20)
    extrude(amount=2, mode= Mode.SUBTRACT)
show(head)

export_stl(head.part , "/Users/softage/Downloads/Stethoscope/head_diaphragm_template.stl")
