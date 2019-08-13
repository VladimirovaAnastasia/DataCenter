from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import format_duration
from datacenter.models import is_visit_long


def storage_information_view(request):
    non_closed_visits = []

    non_closed_visits_from_db = Visit.objects.exclude(leaved_at=None)

    for non_closed_visit in non_closed_visits_from_db:
        duration = format_duration(get_duration(non_closed_visit))
        flag = is_visit_long(non_closed_visit)
        non_closed_visits.append({
            "duration": duration,
            "entered_at": non_closed_visit.entered_at,
            "who_entered": non_closed_visit.passcard.owner_name,
            "is_strange": flag
        })

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
