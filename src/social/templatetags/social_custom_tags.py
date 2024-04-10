from django import template
import os

# START - code was developed with the help of documentation and other external research, please see referenced links.
register = template.Library()

@register.filter
def have_file_extension(file_field, extension):
    # confirm if field is empty
    if not file_field:
        return False

    filename = os.path.basename(file_field.name)
    return filename.lower().endswith(extension.lower())

    # References:
    # https://docs.python.org/3/library/os.path.html#os.path.basename
    # https://docs.djangoproject.com/en/stable/howto/custom-template-tags/#writing-custom-template-filters

# END - code was developed with the help of documentation and other external research, please see referenced links.
