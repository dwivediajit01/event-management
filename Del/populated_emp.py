import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Del.settings")
import django
django.setup()
from testapp.models import Employee

from faker import Faker
f=Faker()

def employe_generate():
    date=f.date()
    ename=f.name()
    cname=f.company()
    role=f.job()
    sal=f.random_int(min=10000,max=60000)
    email=f.email()
    city=f.city()
    addr=f.address()

    Employee.objects.create(date=date,ename=ename,cname=cname,role=role,sal=sal,email=email,city=city,addr=addr)


n=int(input("Enter the no. of records - "))
for i in range(n):
    employe_generate()
print(n,"no. of records created successfully")
