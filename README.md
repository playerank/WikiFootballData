# Wiki Football Data

# Goal

To create a web platform accessible to all to share analytical football data which are processed by users through the [soccerLogger](https://github.com/playerank/soccerLogger)<br/> application.
This data respect the standard format described by the [Pysoccer](https://github.com/playerank/pysoccer)<br/> library.

# Description

In this platform matches are divided into time slot so users can coopearate and split the work.
Once the analysis of a time slot is completed it will be posted to let other users see it and judge it, since the subjective nature of some evaluations,if the analysis reaches a certain number of negative ratings then it will be possible to remove it and to post a new one, otherwise the same number of positive ratings makes the analysis "confirmed".
Once a match is entirely analyzed and the results "confirmed", the data created by registered users will be visible even by unregistered users.

# Requirements

-python version 3.10.4 or later (to verify installation ```$py --version```).
-fastapi version 0.75.2 or later
-mongoengine version 0.24.1 or later
-python-jose version 3.3.0 or later
-passlib 1.7.4 or later

# Author

- author: Edoardo Angelotti
- supervisor: Paolo Cintia
