from django.contrib.auth.mixins import UserPassesTestMixin

# Tozi koito pravi zaqvkata sushtiq li e kato tozi na koito se opitva da otvori profila
class CheckUserIsOwner(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user == self.get_object().user