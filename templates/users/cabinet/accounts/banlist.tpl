{% extends "common/base.tpl" %}

{% block title %}Бан-лист{% endblock %}

{% block content %}
    {% include "common/header.tpl" %}
    <div class="container">
        <table class="table table-light bg-light">
            <thead>
                <th scope="col">#</th>
                <th scope="col">Ник</th>
                <th scope="col">Telegram ID</th>
                <th scope="col">Администратор</th>
                <th scope="col">Причина</th>
            </thead>
        </table>
    </div>
{% endblock %}