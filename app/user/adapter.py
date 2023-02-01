from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class DefaultOverrideAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        You can use this hook to intervene, e.g. abort the login by
        raising an ImmediateHttpResponse

        Why both an adapter hook and the signal? Intervening in
        e.g. the flow from within a signal handler is bad -- multiple
        handlers may be active and are executed in undetermined order.
        """
        # social account already exists, so this is just a login
        # print(dir(request))
        # print(sociallogin.account.extra_data)
        print('yyy', sociallogin.account.extra_data)
        if sociallogin.is_existing:
            return
        email = sociallogin.account.extra_data.get("email", None)


        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        # if it does, connect this new social login to the existing user

        sociallogin.connect(request, user)

    def save_user(self, request, sociallogin, form=None):
        u = super().save_user(request, sociallogin, form=None)
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """

        firstname = sociallogin.account.extra_data.get("firstname", None)
        u.is_active = True
        u.verified = True
        # u.display_name = f'{}'
        u.save()
        return u

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        print('xxxxx', data)
        print(sociallogin)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        name = data.get("name")
        user = sociallogin.user
        name_parts = (name or "").partition(" ")
        display_name = f'{first_name or name_parts[0]} {last_name or name_parts[2]}'
        user_field(user, "firstname", first_name or name_parts[0])
        user_field(user, "lastname", last_name or name_parts[2])
        user_field(user, 'display_name', display_name)
        return super().populate_user(request, sociallogin, data)