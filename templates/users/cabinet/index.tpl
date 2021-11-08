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
            {% endif %}
        </h4>
    </div>
{% endblock %}