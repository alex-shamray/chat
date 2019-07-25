from django.db.models import Count, Max


# https://gist.github.com/victorono/cd9d14b013487b8b22975512225c5b4c
def remove_duplicates(Model, unique_fields):
    """
    Remove duplicate objects where there is more than one field to compare.
    """
    duplicates = Model.objects.values(*unique_fields).order_by().annotate(
        max_id=Max('id'), count_id=Count('id')).filter(count_id__gt=1)

    for duplicate in duplicates:
        Model.objects.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']).delete()
