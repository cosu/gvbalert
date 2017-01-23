import re


def remove_links(text):
    """
    Removes http links from the text
    :param text:
    :return:
    """
    return re.sub(r'http.*(\s|$)?', r'\1', text)


def extract_ride_type(text):
    """
    Extracts the first ride type from the string
    :param text:
    :return:
    """
    regex = re.compile(r'(bus|tram|metro)')
    match = regex.search(text)
    return match.group() if match else None


def extract_lines(text):
    """
    Extracts a list of line services from the text
    :param text:
    :return:
    """
    line_regex = re.compile(r'(\d+)+')
    return line_regex.findall(text)


def extract_event_type(text):
    """

    :param text:
    :return:
    """
    event_type_regex = re.compile(r'verstoring|langzaam|vertraging|druk|omleiding|dienstregeling')
    match = event_type_regex.search(text)
    return match.group() if match else None


def extract_destination(text):
    """
    Extracts destination
    :param text:
    :return:
    """
    regex = re.compile('\(richting (.*)\)')
    match = regex.search(text)
    if match and len(match.groups()) == 1:
        return match.group(1)
    return None


def extract_reason(text):
    regex = re.compile('door (.*)[.]')
    match = regex.search(text)
    if match and len(match.groups()) == 1:
        return match.group(1)
    return None
