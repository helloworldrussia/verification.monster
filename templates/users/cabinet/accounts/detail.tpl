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
                <br />
                 <ul class="list-group">
                    <li class="list-group-item">
                        <b> Фото паспорта </b>
                        <hr />
                        {% if passportfile %}
                            <img width="300" height="500" src="/{{ passportfile.path }}" />
                            <br />
                            <br />
                        {% else %}
                            Фото ещё не было загружено.
                        {% endif %}
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
                        {% if referal_username == "нет" %}
                            Не имеется
                        {% else %}
                            <a href="https://t.me/{{ referal_username }}">
                                @{{ referal_username }}
                            </a>
                        {% endif %}
                    </li>
                    <li class="list-group-item">
                        <b>Вид оплаты:</b> {{ account.type_payment }}
                    </li>
                    <li class="list-group-item">
                        <b>Статус:</b> {% if status|length != 0 %} {{ status.0.status  }}  {% else %} Не принят {% endif %}
                    </li>
                    {% if status|length != 0 %}
                        <li class="list-group-item">
                            <b>Регистратор:</b> 
                            <a href="https://t.me/@{{ status.0.get_registrator_username }}">
                                {{ status.0.get_registrator_username }}
                            </a>
                        </li>
                    {% endif %}
                </ul>
                <br />
                <ul class="list-group">
                    <li class="list-group-item">
                        <form action="" method="POST">
                            <div class="form-group">
                                <label>
                                    <b>Ссылка: </b>
                                </label>
                                <input name="link" {% if account.status == "1" %} disabled value="{{ status.0.link }}" {% endif %} class="form-control" required/>
                            </div>
                            <div class="form-group">
                                <label>
                                    <b>Инструкция: </b>
                                </label>
                                <textarea {% if account.status == "1" %} disabled{% endif %} name="instruction" class="form-control" required>
                                    {% if account.status == "1" %}
                                        {{ status.0.instruction }}
                                    {% endif %}
                                </textarea>
                            </div>
                            {% if account.status == "1" %}
                                <small>
                                    Заявка уже была принята
                                </small>
                                <br />
                            {% endif %}
                            <button class="btn btn-success" type="submit" {% if account.status == "1" or passportfile == None%} disabled{% endif %} >
                                Принять
                            </button>
                            <br />
                            {% if passportfile == None %}
                                <small>Заявка не может быть принята без верификации паспорта!</small>
                            {% endif %}
                        </form>
                    </li>
                </ul>
               

            </div>
        </div>

    </div>
{% endblock%}