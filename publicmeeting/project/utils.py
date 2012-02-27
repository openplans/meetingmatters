from django.template.defaultfilters import slugify

def slugify_uniquely(value, ModelClass, max_length=50):
    """
    Construct a unique slug within the ModelClass objects based on the given
    value.

    """

    slug_suffix = ''
    next_try = 1

    unique_slug = None
    original_slug = slugify(value)[:max_length]
    potential_slug = original_slug

    while unique_slug is None:
        if ModelClass.objects.filter(slug=potential_slug).count() == 0:
            unique_slug = potential_slug

        else:
            next_try += 1
            slug_suffix = '-' + str(next_try)

            prefix_len = min(max_length - len(slug_suffix), len(original_slug))
            potential_slug = original_slug[:prefix_len] + slug_suffix

    return unique_slug