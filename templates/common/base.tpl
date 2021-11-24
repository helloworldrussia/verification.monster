<!DOCTYPE html>
<html lang="ru">
    <head>
        <title>{% block title %}{% endblock %} | Verification</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% load static %}
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        
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