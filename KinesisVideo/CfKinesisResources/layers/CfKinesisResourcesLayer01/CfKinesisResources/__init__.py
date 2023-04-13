import random
import string


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_random_name(event):
    """Generates a random name for the physical resources. 
    Uses a mix of the StackId, Logical Resource Id, and some random string. 
    Finally make sure the whole name is less than 128 characters
    """
    prefix = event['StackId'].split(':')[5].split('/')[1]
    suffix = "-" + event["LogicalResourceId"] + "-" + _get_random_string(8)
    prefix_length = len(prefix)
    suffix_length = len(suffix)
    if prefix_length + suffix_length > 128:
        prefix = prefix[:128-suffix_length]
    return prefix + suffix

__all__ = [
    "get_random_name"
]