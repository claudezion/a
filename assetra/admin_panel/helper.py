import phonenumbers
import markdown

from .countries import countries


def format_mobile(mobile):
    try:
        parsed_number = phonenumbers.parse(mobile)
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    except phonenumbers.phonenumberutil.NumberParseException:
        return mobile


def get_country_name(country_code):
    return countries.get(country_code, country_code)


def convert_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)
