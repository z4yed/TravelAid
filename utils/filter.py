def is_value(parameter):
    return parameter != "" and parameter is not None


def filter_by_address(model, location, district, zip_code):
    queryset = model.objects.all()
    if is_value(location):
        queryset = queryset.filter(address__address__icontains=location.strip())
    if is_value(district):
        queryset = queryset.filter(address__district=district)
    if is_value(zip_code):
        queryset = queryset.filter(address__zip_code=zip_code)
    return queryset


def filter_room(queryset, room_status, room_type, cost_per_day):
    if is_value(room_status):
        queryset = queryset.filter(current_status=room_status)
    if is_value(room_type):
        queryset = queryset.filter(room_type=room_type)
    if is_value(cost_per_day):
        queryset = queryset.filter(cost_per_day__lte=int(cost_per_day))
    return queryset
