{% extends 'common/base.tpl' %}
{% block title %}
    Заявка #{{ account.id }}
{% endblock %}

{% block head %}
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/detail_account.css' %}" />
{% endblock %}

{% block content %}
    {% include 'common/header.tpl' %}
    <div class="container">
        <h3>
            Данные о заявке #{{account.id}}
        </h3>
        <a href="/accounts/take/{{ account.id }}">
            <button class="btn btn-success">
                Принять
            </button>
        </a>
        
        {% if user.get_group == "Администратор" %}
            <a href="/accounts/delete/{{ account.id }}">
                <button class="btn btn-danger">
                    Удалить
                </button>
            </a>
        {% endif %}
        <br />
        <div id="list-params" class="row">
            <div class="col-md-6">
               <ul class="list-group">
                    <li class="list-group-item">
                        <a href="https://t.me/{{ account.tg_username }}">
                            @{{account.tg_username}}
                        </a>
                    </li>
                     <li class="list-group-item">
                        <b>Имя:</b> {{ account.first_name }}
                    </li>
                    <li class="list-group-item">
                        <b>Отчество:</b> {{ account.patronymic }}
                    </li>
                    <li class="list-group-item">
                        <b>Фамилия:</b> {{ account.last_name }}
                    </li>
                    <li class="list-group-item">
                        <b>Страна:</b> {{ account.country }}
                    </li>
                    <li class="list-group-item">
                        <b>Область:</b> {{ account.region }}
                    </li>
                    <li class="list-group-item">
                        <b>Город:</b> {{ account.city }}
                    </li>
                    <li class="list-group-item">
                        <b>Адресс:</b> {{ account.address }}
                    </li>
                    <li class="list-group-item">
                        <b>Дата рождения:</b> {{ account.date_birthday }}
                    </li>
                    
                </ul>
            </div>

            <div class="col-md-6">
                <ul class="list-group">
                     <li class="list-group-item">
                        <b>Документ:</b> {{ account.document_type }}
                    </li>
                    <li class="list-group-item">
                        <b>Реквизиты:</b> {{ account.credit_card }}
                    </li>
                    <li class="list-group-item">
                        <b>Баланс:</b> {{ account.balance }}
                    </li>
                     <li class="list-group-item">
                        <b>Реферал:</b> 
                        <a href="https://t.me/{{ referal_username }}">
                            @{{ referal_username }}
                        </a>
                    </li>
                    <li class="list-group-item">
                        <b>Вид оплаты:</b> {{ account.type_payment }}
                    </li>
                    <li class="list-group-item">
                        <b>Статус:</b> {% if status|length != 0 %} {{ status.status  }}  {% else %} Не принят {% endif %}
                    </li>
                    {% if status|length != 0 %}
                        <li class="list-group-item">
                            <b>Регистратор:</b> {{ status.get_registrator_username }}
                        </li>
                    {% endif %}

                </ul>
            </div>
        </div>

    </div>
{% endblock%}