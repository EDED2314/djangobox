from django.http import JsonResponse
from .models import Location, Box
from django.shortcuts import render


def get_sub_box_data(box):
    """Recursively gather data from sub-boxes."""
    box_data = {
        "name": box.name,
        "url": box.get_absolute_url(),
        "type": "Box",
        "id": box.pk,
        "children": [],
    }

    portions = box.items.all()
    for portion in portions:
        portion_data = {
            "name": f"item <{portion.item.name}>",
            "size": portion.qty,
            "url": portion.get_absolute_url(),
            "type": "Portion",
            "id": portion.pk,
        }
        box_data["children"].append(portion_data)

    subbox_data = []
    subboxes = box.subboxes.all()
    for subbox in subboxes:
        subbox_data.append(get_sub_box_data(subbox))

    box_data["children"].extend(subbox_data)

    return box_data


def get_tree_data(request):
    locations = Location.objects.all()
    tree_data = []

    for location in locations:
        location_data = {
            "name": location.name,
            "url": location.get_absolute_url(),
            "type": "Location",
            "id": location.pk,
            "children": [],
        }

        boxes = location.boxes.all()
        for box in boxes:
            location_data["children"].append(get_sub_box_data(box))

        tree_data.append(location_data)

    return JsonResponse(tree_data, safe=False)


# TODO finish this
def box_selector(request, targetId, type):
    allboxes = Box.objects.all()
    if type == "Location":
        pass
    elif type == "Box":
        pass

    if request.user.is_superuser:
        return render(
            request,
            "actions/boxselector.html",
            {"box_list": allboxes, "targetId": targetId},
        )
    else:
        return render(request, "pages/dashboard.html")
