from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import is_visit_long
from datacenter.models import get_duration
from datacenter.models import format_duration


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.filter(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for visit in visits:
        flag = is_visit_long(visit)
        duration = format_duration(get_duration(visit))
        this_passcard_visits.append({
            "entered_at": visit.entered_at,
            "duration": duration,
            "is_strange": flag
        })

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
