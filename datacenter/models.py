from django.utils import timezone

from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )


def get_duration(visit):
    if visit.leaved_at:
        visit = visit.leaved_at - visit.entered_at
    else:
        now = timezone.now()
        visit = now - visit.entered_at
    return visit


def format_duration(duration):
    hours = duration.seconds // 3600
    minutes = duration.seconds % 3600 // 60
    if duration.days > 0:
        return "{days} д {hours} ч {minutes} мин".format(
            days=duration.days,
            hours=hours,
            minutes=minutes
        )
    else:
        return "{hours} ч {minutes} мин".format(
            hours=hours,
            minutes=minutes
        )


def is_visit_long(visit, minutes=60):
    visit = get_duration(visit).seconds // 60
    return visit > minutes
