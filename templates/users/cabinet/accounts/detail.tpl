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
        {% if account.get_multiaccount_status %}
            <div class="alert alert-danger">
                <b>
                    Подозрение!
                </b>
                <br />
                Данная заявка похожа на остальные 
                {% if account.get_multiaccount_status.first_last_field == "True" %}
                    именем и фамилией!
                {% elif account.get_multiaccount_status.credit_card_field == "True" %}
                    банковской картой!
                {% endif %}
                <br />
                <b>
                    Похожие заявки:
                </b>
                {% for similar_account in account.get_multiaccount_status.get_similar_accounts %}
                    {% if forloop.last %}
                        
                    {% else %}
                        <a href="/accounts/view/{{ similar_account.id }}">
                            Заявка №{{ similar_account.id }}
                        </a>
                    {% endif %}
                {% endfor %}
            </div>
        {% endif %}
        
        <h3>
            Данные о {% if account.status == "ref_account:1" %} реферальной {% endif %}заявке #{{account.id}}
        </h3>
        <a href="/accounts/setbalance/{{ account.id }}">
            <button class="btn btn-success">
                Установить баланс
            </button>
        </a>
        {% if user.get_group == "Администратор" %}
            <a href="/accounts/delete/{{ account.id }}">
                <button class="btn btn-danger">
                    Удалить
                </button>
            </a>
            <a href="/accounts/banlist/add/{{ account.id }}">
                <button class="btn btn-danger">
                    Забанить
                </button>
            </a>
        {% endif %}
        <br />

        {% if account.status == "ref_account:1" %}
            <div id="list-params" class="row">
                <div class="col-md-6">
                    <ul class="list-group">
                        <li class="list-group-item">
                            <a href="https://t.me/{{ account.tg_username }}">
                                @{{account.tg_username}}
                            </a>
                        </li>
                        <li class="list-group-item">
                            <b>Имя: </b> {{ account.first_name }}
                        </li>
                         <li class="list-group-item">
                            <b>Фамилия: </b> {{ account.last_name }}
                        </li>

                         <li class="list-group-item">
                            <b>Баланс: </b> {{ account.balance }}
                        </li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <ul class="list-group">
                        <li class="list-group-item">
                            <b>Всего привёл: </b>
                            {{ count_referals_by_account }}
                        </li>
                        <li class="list-group-item">
                            <b>Реферальная ссылка: </b>
                            <a href="https://{{ blank_referals }}{{account.tg_id}}">
                                {{ blank_referals }}{{account.tg_id}}
                            </a>
                        </li>
                    </ul> 
                </div>
            </div>
        {% else %}
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
                    {% if account.status == "drop" or account.status == "drop_done" %}
                        <li class="list-group-item">
                            <b>Дроповод: </b>
                            <a href="https://t.me/{{ account.get_drop_user.username }}">
                                @{{ account.get_drop_user.username }}
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
                                <input name="link" {% if account.status == "1" or account.status == "drop_done" %} disabled value="{{ status.0.link }}" {% endif %} class="form-control" required/>
                            </div>
                            <div class="form-group">
                                <label>
                                    <b>Инструкция: </b>
                                </label>
                                <textarea {% if account.status == "1" or account.status == "drop_done" %} disabled{% endif %} name="instruction" class="form-control" required>
                                    {% if account.status == "1" %}
                                        {{ status.0.instruction }}
                                    {% endif %}
                                </textarea>
                            </div>
                            {% if account.status == "1" or account.status == "drop_done" %}
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
        {% endif %}
        

    </div>
{% endblock%}