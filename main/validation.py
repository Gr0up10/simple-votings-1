from django.utils.text import format_lazy
from django.utils.translation import ugettext as _


def get_field_too_long_string(name, len):
    return format_lazy("{name} text is too long, maximum length is {len}", name=name, len=len)


def get_field_should_be_filled_string(name):
    return format_lazy("{name} should be filled", name=name)


NAME_MAX_LENGTH = 100
DESC_MAX_LENGTH = 500
CHOICE_MAX_LENGTH = 100


def validate_field(field, name, max_len):
    if len(field) > max_len:
        return get_field_too_long_string(name, max_len)
    if len(field) == 0:
        return get_field_should_be_filled_string(name)


def validate_voting(voting):
    val = validate_field(voting['title'], _('Title field'), NAME_MAX_LENGTH)
    if val:
        return val
    val = validate_field(voting['description'], _('Description field'), DESC_MAX_LENGTH)
    if val:
        return val

    if len(voting['choices']) < 2:
        return _('There are should be at least two choices')

    if voting['choice_type'] > 1:
        return _('Choice type should be binary')

    for i, choice in enumerate(voting['choices']):
        val = validate_field(choice, format_lazy('Choice number {num}', i), CHOICE_MAX_LENGTH)
        if val:
            return val
