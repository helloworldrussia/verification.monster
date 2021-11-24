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
        
        <div class="row">
            <div class="col-md-6">
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
            </div>
            <div class="col-md-6">
                <p>
                    Статусы:
                    <small class="text-danger">
                        подозрение на мульти аккаунт
                    </small>
                    ;
                    <small class="text-success">
                        принято
                    </small>
                    ;
                    <small class="text-warning">
                        не загруженно фото
                    </small
                </p>
            </div>
        </div>
        
        <table class="table table-light table-hover">
            <thead>
                <tr>
                    <th>
                    
                    </th>
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
                    <tr 
                    {% if account.get_multiaccount_status != None %} class="table-danger" {% endif %}
                    {% if account.get_passport_file_status == None and account.status != "ref_account:1" and account.status != "ref_account:-1" and account.status != "drop" and account.status != "drop_done" %} class="table-warning" {% endif%}
                    {% if account.status == '1' or account.status == "drop_done" %} class="table-success" {% endif %}
                    >
                        <td>
                            <small>
                                {% if account.status == "drop" or account.status == "drop_done" %}
                                    {{ account.get_drop_datetime }}
                                {% else %}
                                    {{ account.get_datetime }}
                                {% endif %}
                            </small>
                        </td>
                        <th scope="row"> {{ account.id }}</th>
                        <td>
                            <a href="https://t.me/{{ account.tg_username }}">
                                @{{ account.tg_username }}
                            </a>
                        </td>
                        {% if account.status == "None" or account.status == "1" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>{{ account.document_type }}</td>
                            <td>{{ account.type_payment }}</td>
                            <td>
                                <a href="/accounts/view/{{ account.id }}">
                                    Подробнее
                                </a>
                            </td>
                        {% elif account.status == "-1" %}
                            <td>
                                <p class="text-warning">
                                    в процессе
                                </p>
                            </td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td>
                                <a href="/accounts/delete/{{ account.id }}" class="text-danger">
                                    <p class="text-danger">Удалить</a>
                                </a>
                            </td>
                        {% elif account.status == "ref_account:1" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>
                                <p class="text-primary">
                                    Реферальная заявка
                                </p>
                                <td></td>
                                <td>
                                    <a href="/accounts/view/{{ account.id }}">
                                        Подробнее
                                    </a>
                                </td>

                            </td>
                        {% elif account.status == "ref_account:-1" %}
                            <td>
                            <p class="text-primary">
                                Реферальная заявка <span class="text-warning">(в процессе)</span>
                            </p>
                            </td>
                            <td></td>
                            <td>
                            </td>

                            </td>
                        {% elif account.status == "drop" or account.status == "drop_done" %}
                            <td>{{ account.first_name }}</td>
                            <td>{{ account.last_name }}</td>
                            <td>{{ account.document_type }}</td>
                            <td>{{ account.type_payment }}</td>
                            <td>
                                <a href="/accounts/view/{{ account.id }}">
                                    Подробнее
                                </a>
                            </a>
                            
                        {% endif %}
                        
                    </tr>
                {% endfor %}




            </tbody>

        </table>
    </div>

{% endblock %}
