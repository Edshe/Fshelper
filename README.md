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
    endpoint_url=endpoint_url
}
# Creating cloud directory instance
aws = CloudDirectory(**params)

# Getting a list of folders and files
aws.ls_files()
aws.ls_folders()

# Finding all images
aws.find(mask='*jpg').get('files')


```

