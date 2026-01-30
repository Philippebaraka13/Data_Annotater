from django.shortcuts import render

# Create your views here.

import csv
import io

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CSVUploadForm, RetailRowAnnotateForm
from .models import RetailRow


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]

            text = uploaded.read().decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))

            inserted = 0
            skipped = 0

            for row in reader:
                merchant = (row.get("merchant") or "").strip()
                sku = (row.get("sku") or "").strip()
                country = (row.get("productcountry") or "").strip().upper()

                if not (merchant and sku and country):
                    continue

                try:
                    with transaction.atomic():
                        RetailRow.objects.create(
                            merchant=merchant,
                            sku=sku,
                            country=country,
                        )
                    inserted += 1
                except IntegrityError:
                    skipped += 1

            messages.success(
                request,
                f"Upload complete. Inserted {inserted}, skipped {skipped} duplicates."
            )
            return redirect("annotater:pending_list")
    else:
        form = CSVUploadForm()

    return render(request, "annotater/upload.html", {"form": form})


def pending_list(request):
    rows = RetailRow.objects.all().order_by("segment", "merchant")
    return render(request, "annotater/pending_list.html", {"rows": rows})


def edit_row(request, pk):
    obj = get_object_or_404(RetailRow, pk=pk)

    if request.method == "POST":
        form = RetailRowAnnotateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Row updated successfully.")
            return redirect("annotater:pending_list")
    else:
        form = RetailRowAnnotateForm(instance=obj)

    return render(request, "annotater/edit_row.html", {"form": form, "obj": obj})
