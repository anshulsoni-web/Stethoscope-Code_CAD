# Stethoscope Design
Design of a stethoscope using the build123d Python library. 
This document contains a replica of a stethoscope design. The design was created using the Build123D Python library. 
First, build123d was imported into VSCode, then the OCP viewer was imported to help us visualize the design in real time. 
Then, assigned values to key variables such as length, height, and thickness that will be used to define the body further. 
First, build the base sketch using the "buildsketch" command for part of the design. Then, extrude it by defining it as a base body using the "buildpart" command. After that, using the base sketch as a base plane, moving ahead with drawing sketches and extruding them to shape the body as desired. 
To extrude, "mode.ADD" is used, and to extrude cut, "mode.SUBTRACT" is used. This is an important part, and if we do not define mode, the library defaults to "mode.ADD" with extrude. 
To apply a chamfer or fillet, the plane is defined first, and then the "chamfer" command is simply applied. 
To make a cylinder, circle, rectangle, ellipse, or any shape, its "centre point" is fed a "location" command, and then the extrude or extrude cut is defined using extrude mode.ADD or mode.Subtract command.
To make a tube along a zigzag path, a path was defined first, then a sketch was made and then sweep command was applied to sweep the sketch along that path. 
For a rectangle, the centre point of the rectangle is, by default, considered in this library. Later, in parentheses, the first "length of rectangle along X axis" is fed and the latter is considered as "width along Y axis". This is the same for an ellipse, the first radius is processed along the X axis and then next along Y axis, separated by a comma. 
At last, extracting the solid body from the buildpart context manager using the name used to define the body in the beginning and storing it in a variable named result_part.
Using the show(result_part) feature of the OCP viewer, the body was visualised in VS Code.  
Later, the volume was measured and compared with the reference design to measure the volumetric difference. 
