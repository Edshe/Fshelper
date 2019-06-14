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
Also you can install ```virtualenvwrapper``` through pip.



**Clone the source of the project**

```
git clone https://github.com/Edshe/Fshelper
```

**Install dependencies**

```
cd Fshelper
mkvirtualenv fshelper
workon fshelper
pip install -r requirements.txt
```

**Usage**

```
# Specifying your aws credentials
params={
    service_name='s3',
    aws_access_key_id=your_aws_key_id,
    aws_secret_access_key=your_aws_secret_access_key,
    config=Config(
        s3={'use_accelerate_endpoint': accelerate_endpoint}
    ),
    endpoint_url=endpoint_url  # for IBM
}

# Creating cloud directory instance
aws = CloudDirectory(**params)

# Getting a list of folders and files
aws.ls()
aws.ls_files()
aws.ls_folders()

# Finding all images
aws.find(mask='*jpg').get('files')

# Moving to next directory
aws.cd('myfolder')

# Reading and saving a file content
file = aws.ls_files()[0]
file.read()  # reading the file content to _file variable
file.save()  # saving  the file content to aws


```
Full list of methods you can see in abstract classes inside base.py

