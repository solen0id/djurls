# djurls - A simple Django URL Shortener

This is a small sample project to showcase some of the things I learned while working
with Django and DRF.

## What is it?

You are looking at djurls, a simple **Dj**ango **URL** **S**hortener.  
This project is intended to showcase how easy it is to get up  
and running with [Django](https://www.djangoproject.com/) and
[Django Rest Framework](https://www.django-rest-framework.org/).  

Apart from Django and DRF, the only other dependencies use are [pytest](https://docs.pytest.org/en/stable/)
and [pytest-django](https://pytest-django.readthedocs.io/en/latest/).

## What does it do?
What is a URL shortener you ask? Well, it is a service that turns a long URL like,  
http://www.thisisaverylongurl.com/?and=it-also-contains&query_parameters into  
a much shorter URL like http://yourhost.com/r/vJKd3y, which still redirects a user to  
the original resource when accessed.  

At its core, djurls consists of two endpoints:
1. `/api/urls/`: Allows users to POST a URL and receive a shortened URL in return
2. `/r/`: Redirects users to the original URL used when the shortened URL was created

Some of its other features, in no particular order, include:
- Authenticated users can list shortened URLs they created previously at `/api/urls/`
- Authenticated users see how many times a shortened URLs they created was accessed
- Query parameters are preserved when accessing a shortened url
- The shortened URL will always contain the address of the host running the service
- The short keys used in redirect URLs start out with a length of just a single character


## How do I run it?

To run the project locally, simply:
1. Install the required dependencies with `pip install -r requirements.txt`
2. Bring up the development webserver with `python djurls/manage.py runserver`
3. Tweak `djurls/settings.py` and the project to your liking (Optional)
4. POST or browse to http://localhost:8000/api/urls to create a shortened URL
    1. When posting, the only required field in the request body is `url`.  
    Make sure that the provided value is a valid URL, as it will be validated by
    the serializer
    2. Browsing to http://localhost:8000/api/urls lets you create shortened URLs with
    DRFs Browsable API
