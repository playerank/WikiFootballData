# Wiki Football Data

# Goal

To create a web platform accessible to all to share analytical football data which are processed by users through the [soccerLogger](https://github.com/playerank/soccerLogger)<br/> application.
This data respect the standard format described by the [Pysoccer](https://github.com/playerank/pysoccer)<br/> library.

# Description

In this platform matches are divided into time slot so users can coopearate and split the work.
Once the analysis of a time slot is completed it will be posted to let other users see it and judge it, since the subjective nature of some evaluations,if the analysis reaches a certain number of negative ratings then it will be possible to remove it and to post a new one, otherwise the same number of positive ratings makes the analysis "confirmed".
Once a match is entirely analyzed and the results "confirmed", the data created by registered users will be visible even by unregistered users.

# Requirements

-python version 3.10.4 or later (to verify installation ```sh $py --version```)<br>
-fastapi version 0.75.2 or later<br>
-mongoengine version 0.24.1 or later<br>
-python-jose version 3.3.0 or later<br>
-passlib 1.7.4 or later<br>

# Guide
1. Check if python is arleady installed in your pc<br/>
2. Install all necessary dependencing with [pip](https://pypi.org/project/pip/)<br/>
```sh
$ py -m pip install -r requirements.txt
```
3. Move in back_end<br/>
```sh
$ cd "back_end"
```
4. Run<br/>
```sh
$ uvicorn mainAPI:app --reload
```
Once launched, on your shell, you should have a success message such as the following:
![bash](/Scheme/bash.png)<br/>
5. Now you can interact with the Database from a browser, adding ```/docs``` or ```/redocs``` to the following url: ```http://127.0.0.1:8000```, you will see the automatic generated docs by [fastAPI](https://fastapi.tiangolo.com/)

# Author

- author: Edoardo Angelotti
- supervisor: Paolo Cintia
