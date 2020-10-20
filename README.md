Make sure you have: 
- Docker installed 
- repository copied to your local machine 

first run to build project locally: 

```
docker-compose up --build 
```

next time: 

```
docker-compose up 
``` 
is enough.

To create superuser: 
```
docker-compose exec web sh
``` 

```
python manage.py createsuperuser
``` 
and follow instructions

