Simply dialog system
=======================


Author:
    E.Shemakhov

Status:
    in development




About:
-----

Module helps to work with AWS, IBM and local file system.
 




Requirements:
-----

-   ibm-cos-sdk==2.4.4
-   boto3==1.9
-   botocore==1.12





How to install:
-----

Make sure that ```python 3.6```, ```virtualenv```, ```pip``` installed and updated.
Also install ```virtualenvwrapper``` through pip.



**Clone the source of the project**

```
git clone https://github.com/Edshe/Fshelper
```

**Install dependencies**

```
cd Fshelper
mkvirtualenv dialogtest
workon dialogtest
pip install -r requirements.txt
```

**Launch**

```
python manage.py runserver
```

**Run tests**

```
python manage.py test
```





Apps:
-------------

**Questionnaires**:
	
Main questionnaire models: **Questionnaire**, **Question**, **Choice**.
Provides API for getting Questionnaires list, Questionnaire details, Question details Contains task for creating Questionnaires from json file. "data.json" - file example is in project folder. 

**Users**:
	
Models: **User**
Provides views for authorization and home page view.


**Dialogs**:
	
Models: **Dialog**, **UserAnswer**
Provides API for getting Dialogs list, Dialog details
and API to create new UserAnswer



Front-end:
-------------

Django-templates + vue.js

