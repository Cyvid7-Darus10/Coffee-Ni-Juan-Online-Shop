from decouple import config

def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


LETTERS = config('ENCRYPT_LETTERS')
WORD = config('SECRET_WORD')
KEY = config('ENCRYPT_KEY')
key = KEY.split(',')

def encrypt(message):
    encrypted = encrypt_recur(message, 0, 1)
    # encrypted = second_layer(encrypted)
    encrypted = second_layer(encrypted)
    encrypted = encrypt_recur(encrypted, 0, 1)
    return encrypted
    
def decrypt(message):
    decrypted = decrypt_recur(message, 0, 1)
    # decrypted = decrypted.replace(WORD, '')
    decrypted = decrypted.replace(WORD, '')
    decrypted = decrypt_recur(decrypted, 0, 1)
    return decrypted

def encrypt_recur(message, start, over):
    if start == over: return message
    else: start += 1
    
    encrypted = ''
    i = 0
    for chars in message:
        if chars in LETTERS:
            if i == len(key) - over:
                i = 0
            num = LETTERS.find(chars)
            num += int(key[i + start])
            encrypted +=  LETTERS[num]
            i += 1
            
    return encrypt_recur(encrypted, start, over)

def second_layer(message):
    encrypted = ''
    i = 0
    for chars in message:
        if chars in LETTERS:
            if i == len(key):
                i = 0
            if key[i] == '9':
                encrypted += WORD
            encrypted += chars
            i += 1
    return encrypted

def decrypt_recur(message, start, over):
    if start == over: return message
    else: start += 1
        
    decrypted = ''
    i = 0
    for chars in message:
        if chars in LETTERS:
            if i == len(key) - over:
                i = 0
            num = LETTERS.find(chars)
            num -= int(key[i + start])
            decrypted +=  LETTERS[num]
            i += 1
            
    return decrypt_recur(decrypted, start, over)
