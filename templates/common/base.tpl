<!DOCTYPE html>
<html lang="ru">
    <head>
        <title>{% block title %}{% endblock %} | Verification</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% load static %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="{% static 'css/base.css' %}" />
        {% block head %}
        {% endblock %}

    </head>
    <body>
        <div id="content">
        {% block content %}
        {% endblock %}
        </div>



        {% block scripts %}{% endblock %}
        <script src="{% static 'scripts/jquery-3.3.1.slim.min.js' %}"></script>
        <script src="{% static 'scripts/popper.min.js' }"></script>
        <script src="{% static 'scripts/bootstrap.min.js' %}"></script>
    </body>
</html>