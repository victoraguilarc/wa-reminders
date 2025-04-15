def overload_properties(
    instance: object,
    validated_data: dict[str, any],
):
    for _property, _value in validated_data.items():
        if not hasattr(instance, _property):
            continue
        setattr(instance, _property, _value)
