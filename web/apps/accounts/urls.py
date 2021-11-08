from django.urls import path
from .views import all_view, detail_view, delete_view, take_view

urlpatterns = [
    path("<str:show_type>/", all_view, name="view_all_accounts"),
    path("view/<int:account_id>", detail_view, name="detail_accounts_view"),
    path("delete/<int:account_id>", delete_view, name="delete_account"),
    path("take/<int:account_id>", take_view, name="take_account")
]
