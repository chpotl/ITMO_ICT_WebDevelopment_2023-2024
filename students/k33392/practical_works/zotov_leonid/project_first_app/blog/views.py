from django.http import Http404
from django.shortcuts import render
from .models import CustomUser


def detail(request, owner_id):
    try:
        owner = CustomUser.objects.get(pk=owner_id)
        driver_licence = owner.licences.order_by("-issue_date").first()
    except CustomUser.DoesNotExist:
        raise Http404("Автовладельца не существует!")
    return render(
        request,
        "project_first_app/detail.html",
        {"owner": owner, "driver_licence": driver_licence}
    )
