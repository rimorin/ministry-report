from django.http import Http404
from django.shortcuts import render
from congregation.models import Congregation, Group, Publisher
from ministry.models import Report
from .forms import ReportForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dal import autocomplete
from django.contrib.auth.decorators import login_required
import calendar

DEFAULT_CONGREGATION = "wlnorth"
DEFAULT_CONG_GROUP = 3
DEFAULT_LOGIN_URL = "/admin/login/?next=/admin/"


class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return item.name

    def get_queryset(self):
        qs = Publisher.objects.all()
        if self.q:
            qs = qs.filter(
                group__congregation__code=self.forwarded.get(
                    "code", DEFAULT_CONGREGATION
                ),
                name__icontains=self.q,
            )
        return qs


def get_date(year=None, month=None):
    if not year and not month:
        day_last_month = datetime.today() - relativedelta(months=1)
        year = day_last_month.year
        month = day_last_month.month
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, calendar.monthrange(year, month)[1])

    return start_date, end_date


@login_required(login_url=DEFAULT_LOGIN_URL)
def get_report(request, group_id=DEFAULT_CONG_GROUP, year=None, month=None):

    groups = set([group.name for group in request.user.groups.all()])
    group = Group.objects.get(pk=group_id)

    if group.congregation.code not in groups:
        raise PermissionError("You are not authorized to view this report")

    start_date, end_date = get_date(year=year, month=month)
    # if not month:
    #     date_to_display = end_date - relativedelta(months=1)

    group_publishers = Publisher.objects.filter(group_id=group_id)

    for publisher in group_publishers:
        publisher_report = Report.objects.filter(
            creation_date__gte=start_date,
            creation_date__lte=end_date,
            publisher=publisher,
        ).first()
        publisher.report = publisher_report
    return render(
        request,
        "reports.html",
        {
            "publishers": group_publishers,
            "month": calendar.month_name[end_date.month],
            "year": end_date.year,
        },
    )


def cong_submission(request, congregation_code=DEFAULT_CONGREGATION):
    if not Congregation.objects.filter(code=congregation_code).exists():
        raise Http404("Congregation does not exist")

    if not request.method == "POST":
        return render(
            request,
            "submission.html",
            {"form": ReportForm(), "congregation_code": congregation_code},
        )
    # create a form instance and populate it with data from the request:
    form = ReportForm(request.POST)

    if not form.is_valid():
        return render(request, "submission.html", {"form": form})

    start_date, end_date = get_date()
    selected_publisher = form.cleaned_data["publisher"]
    existing_report = Report.objects.filter(
        creation_date__gte=start_date,
        creation_date__lte=end_date,
        publisher=selected_publisher,
    ).first()

    if "create_next_month" in request.POST:
        existing_next_month_report = Report.objects.filter(
            creation_date__gt=end_date,
            publisher=selected_publisher,
        ).first()
        if existing_next_month_report:
            existing_next_month_report.hours = form.cleaned_data["hours"]
            existing_next_month_report.placements = form.cleaned_data["placements"]
            existing_next_month_report.bible_studies = form.cleaned_data[
                "bible_studies"
            ]
            existing_next_month_report.return_visits = form.cleaned_data[
                "return_visits"
            ]
            existing_next_month_report.videos = form.cleaned_data["videos"]
            existing_next_month_report.remarks = form.cleaned_data["remarks"]
            existing_next_month_report.save()
        else:
            new_report = form.save()
            new_report.creation_date = start_date + relativedelta(months=1)
            new_report.save()

    if "update_existing" in request.POST:
        existing_report.hours = form.cleaned_data["hours"]
        existing_report.placements = form.cleaned_data["placements"]
        existing_report.bible_studies = form.cleaned_data["bible_studies"]
        existing_report.return_visits = form.cleaned_data["return_visits"]
        existing_report.videos = form.cleaned_data["videos"]
        existing_report.remarks = form.cleaned_data["remarks"]
        existing_report.save()

    if "submit_report" in request.POST:
        if existing_report:
            return render(
                request,
                "existing.html",
                {
                    "form": form,
                    "month": calendar.month_name[end_date.month],
                    "year": end_date.year,
                },
            )
        form.save()

    return render(request, "thanks.html", {"name": selected_publisher.name})
