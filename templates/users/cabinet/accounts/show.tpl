{% extends 'common/base.tpl' %}
{% block title %}
    Список заявок
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h4>
            Список заявок
        </h4>
        
        <ul class="nav">
            {% if request.user.get_group == "Администратор" %}
            <li class="nav-item">
                <a href="/accounts/all" class="nav-link">
                    Все
                </a>
            </li>
            <li class="nav-item">
                <a href="/accounts/completed" class="nav-link">
                    Принятые
                </a>
            </li>
            {% endif %}
             <li class="nav-item">
                <a href="/accounts/new" class="nav-link">
                    Не принятые
                </a>
            </li>

            <li class="nav-item">
                <a href="/accounts/my" class="nav-link">
                    Мои
                </a>
            </li>
        </ul>

        <table class="table table-light table-hover">
            <thead>
                <tr>
                    <th scope="col">
                        #
                    </th>
                    <th scope="col">
                        Ник
                    </th>
                    <th scope="col">
                        Имя
                    </th>
                    <th scope="col">
                        Фамилия
                    </th>
                    <th scope="col">
                        Документ
                    </th>
                    <th scope="col">
                        Тип оплаты(грн.)
                    </th>
                     <th scope="col">
                        Действия
                    </th>
                </tr>
            </thead>
            <tbody>
                {% for account in accounts %}
                    <tr>
                        <th scope="row"> {{ account.id }}</th>
                        <td>
                            <a href="https://t.me/{{ account.tg_username }}">
                                @{{ account.tg_username }}
                            </a>
                        </td>
                        <td>{{ account.first_name }}</td>
                        <td>{{ account.last_name }}</td>
                        <td>{{ account.document_type }}</td>
                        <td>{{ account.type_payment }}</td>
                        <td>
                            <a href="/accounts/view/{{ account.id }}">
                                Подробнее
                            </a>
                        </td>
                    </tr>
                {% endfor %}




            </tbody>

        </table>
    </div>

{% endblock %}
