from decouple import config
from management.models import Analytic


LETTERS = config('ENCRYPT_LETTERS')
WORD = config('SECRET_WORD')


def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


def record_analytic(request, action_type, description):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    
    if request.user.is_authenticated:
        Analytic.objects.create(user=request.user, action_type=action_type, ip_address=ip_address, description=description)
    else:
        Analytic.objects.create(action_type=action_type, ip_address=ip_address, description=description)


def encrypt(message):
    encrypted_message = ''
    for char in message:
        if char in LETTERS:
            index = LETTERS.index(char)
            encrypted_message += WORD[index]
        else:
            encrypted_message += char
    
    return encrypted_message
    
    

def decrypt(message):
    decrypted_message = ''
    for char in message:
        if char in WORD:
            index = WORD.index(char)
            decrypted_message += LETTERS[index]
        else:
            decrypted_message += char

    return decrypted_message