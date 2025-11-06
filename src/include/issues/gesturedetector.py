import flet as ft


def trigger_open_menu(
    event: ft.TapEvent[ft.GestureDetector] | ft.LongPressStartEvent[ft.GestureDetector],
):
    print(event)


async def main(page: ft.Page):
    # on web, disable default browser context menu
    if page.web:
        await page.browser_context_menu.disable()

    gd = ft.GestureDetector(
        on_long_press_start=trigger_open_menu,
        on_secondary_tap=trigger_open_menu,
        content=ft.ListTile(title=ft.Text("Test"), subtitle=ft.Text("Testing")),
    )
    page.add(gd)


if __name__ == "__main__":
    ft.run(main)
