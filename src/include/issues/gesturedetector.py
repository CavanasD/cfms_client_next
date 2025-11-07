import flet as ft


def trigger_open_menu(
    event: ft.TapEvent[ft.GestureDetector] | ft.LongPressStartEvent[ft.GestureDetector],
):
    print(event)

def handle_on_tap(event: ft.Event[ft.GestureDetector]):
    print("Tapped")

def handle_on_tap_down(event: ft.Event[ft.GestureDetector]):
    print("Tapped down")

def handle_on_click(event: ft.Event[ft.ListTile]):
    print("Tile clicked")


async def main(page: ft.Page):
    # on web, disable default browser context menu
    if page.web:
        await page.browser_context_menu.disable()

    gd = ft.GestureDetector(
        on_long_press_start=trigger_open_menu,
        on_secondary_tap=trigger_open_menu,
        on_tap=handle_on_tap,
        on_tap_down=handle_on_tap_down,
        content=ft.ListTile(
            title=ft.Text("Test"),
            subtitle=ft.Text("Testing"),
            on_click=handle_on_click,
        ),
    )
    page.add(gd)


if __name__ == "__main__":
    ft.run(main)
