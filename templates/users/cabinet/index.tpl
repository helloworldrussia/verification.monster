{% extends 'common/base.tpl' %}

{% block title %}
    Личный кабинет 
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h2>
            {{ user.first_name }} {{ user.last_name }}
        </h2>
        <p>
            {{ user.get_group }}
        </p>

        <br />

        <h2>
            Статистика
        </h2>
        <hr />
        <h4 align="center">
            {% if user.get_group == "Администратор" %}
                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во заявок в настоящий момент:
                                </h6>
                                {{ all_accounts_count }}
                            </div>
                        </div>
                    </div>
                     <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего принятых заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во принятых заявок:
                                </h6>
                                {{ completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Всего сотрудников</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Кол-во сотрудников:
                                </h6>
                                {{ all_users_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <h2>
                    Сегодня
                </h2>
                <hr />
                <div class="row">
                     <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Принято заявок</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Принято заявок за сегодня:
                                </h6>
                                {{ today_completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">За вчера</h5>
                                <hr />
                                <h6 class="card-subtitle md-2 text-muted">
                                    Принято заявок за вчера:
                                </h6>
                                {{ yesterday_completed_accounts_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <br />
                <h2>
                    Регистраторы
                </h2>
                <hr />
                <div class="row">
                    {% for registrator in registrator_completed_accounts %}
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a href="https://t.me/{{ registrator.tg_username }}">
                                            @{{ registrator.tg_username }}
                                        </a>
                                    </h5>
                                    <hr />
                                    <h6 class="card-subtitle md-2 text-muted">
                                        Выполнено заявок:
                                    </h6>
                                    {{ registrator.count }} 
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        </h4>
    </div>
{% endblock %}