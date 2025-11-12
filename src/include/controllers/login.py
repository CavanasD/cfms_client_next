from typing import TYPE_CHECKING

from include.classes.config import AppConfig
from include.ui.controls.dialogs.admin.accounts import PasswdUserDialog
from include.util.requests import do_request

if TYPE_CHECKING:
    from include.ui.controls.views.login import LoginForm

from include.util.locale import get_translation

t = get_translation()
_ = t.gettext


class LoginFormController:
    def __init__(self, view: "LoginForm"):
        self.view = view
        self.app_config = AppConfig()

    async def action_login(self):
        await self._action_login()
        self.view.enable_interactions()

    async def _action_login(self):
        username = self.view.username_field.value.strip()
        password = self.view.password_field.value

        response = await do_request(
            "login",
            {
                "username": username,
                "password": password,
            },
        )

        if (code := response["code"]) == 200:
            self.app_config.username = username
            self.app_config.nickname = response["data"].get("nickname")
            self.app_config.token = response["data"]["token"]
            self.app_config.token_exp = response["data"].get("exp")
            self.app_config.user_permissions = response["data"]["permissions"]
            self.app_config.user_groups = response["data"]["groups"]

            self.view.clear_fields()

            await self.view.page.push_route("/home")

        elif code == 403:
            self.view.page.show_dialog(
                PasswdUserDialog(
                    username, tip=_("Password must be changed before login.")
                )
            )
            return

        else:
            self.view.send_error(
                _("Login failed: ({code}) {message}").format(
                    code=code, message=response["message"]
                )
            )
