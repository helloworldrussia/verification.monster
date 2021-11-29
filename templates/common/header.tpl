<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="#">Admin</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="/user">
                    Мой кабинет
                </a>
            </li>
            {% if request.user.get_group == "Регистратор" %}
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/new">
                        Заявки
                    </a>
                </li>
            {% endif %}
            {% if request.user.get_group == "Администратор" %}
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/all">
                        Заявки
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/user/list">
                        Сотрудники
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/accounts/banlist">
                        Бан-лист
                    </a>
                </li>
            {% endif %}
            {% if request.user.get_group == "Дроповод" %}
                <li class="nav-item">
                    <a class="nav-link" href="/drop/create">
                        Создать заявку
                    </a>
                </li>
            {% endif %}
                <li class="nav-item">
                    <a class="nav-link" href="/user/logout">
                        Выйти
                    </a>
                </li>
            </ul>
        </div>

    </div>
</nav>