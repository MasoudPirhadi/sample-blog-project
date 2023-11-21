from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokensGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.is_active}{user.pk}{timestamp}"


activation_token = TokensGenerator()
