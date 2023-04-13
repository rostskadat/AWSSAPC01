import random
import string


def get_random_name(event):
    """Generates a random name for the physical resources. 

    Uses a mix of the StackId, Logical Resource Id, and some random string. 
    Finally make sure the whole name is less than 128 characters

    Args:
        event (dict): The CloudFormation event

    Returns:
        string: the newly generated random name
    """
    prefix = event['StackId'].split(':')[5].split('/')[1]
    suffix = "-" + event["LogicalResourceId"] + "-" + get_random_string(8)
    prefix_length = len(prefix)
    suffix_length = len(suffix)
    if prefix_length + suffix_length > 128:
        prefix = prefix[:128-suffix_length]
    return prefix + suffix

def get_random_string(length):
    """Returns a random string of the specified length.

    The string will be composed of uppercase ASCII characters and digits.

    Args:
        length (int): the desired length of the random string

    Returns:
        string: a random string
    """    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))



__all__ = [
    "get_random_name",
    "get_random_string"
]