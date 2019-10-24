from .models import UserWithCryptoKey
import logging

class AuthBackendWithCryptoKey(object):
    def authenticate(self, email, private_key): 
        try:
            user = UserWithCryptoKey.objects.get(private_key=private_key)
        except UserWithCryptoKey.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " % login)
            return None

    def get_user(self, private_key):
        try:
            user = UserWithCryptoKey.objects.get(private_key=private_key)
            if user.is_active:
                return user
            return None
        except UserWithCryptoKey.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None