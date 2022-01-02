###Creating Graphs for MIT Classes

This project aims to create dependency graphs for the classes in various majors at MIT, like the one shown below for MIT's Physics Major
![image](course-8-graph.png)


The aim is to eventually create a web application for users to select a major and then see the corresponding dependency graph for that major.
When it's complete, the application will also have hyperlinks to each class's description.


Some simplifications were made to this model. Some classes in a major depend on classes outside of that major. For example
8.04 Quantum Physics I (a physics course) is dependent on 18.03 Differential Equations (a math course). Those dependencies were
ignored for visual simplicity. Also, some more advanced classes only require "permission of instructor." Those classes were also ignored
because they are not taken by the average undergraduate at MIT and also have no implementable dependency.


Hope you enjoy!