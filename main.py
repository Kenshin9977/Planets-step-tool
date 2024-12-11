import flet as ft


def main(page: ft.Page):
    original_width = 1920
    original_height = 1080

    click_order = []

    def on_click(e):
        astre_name = e.control.data
        if astre_name in click_order:
            click_order.remove(astre_name)
        else:
            click_order.append(astre_name)

        update_positions()

        order_label.value = " → ".join(click_order)
        page.update()

    def reset_selection(_):
        nonlocal click_order
        click_order = []
        update_positions()
        order_label.value = ""
        page.update()

    def update_positions():
        window_width = page.window.width
        window_height = page.window.height
        width_ratio = window_width / 16
        height_ratio = (window_height - 120) / 9

        scale_factor = (
            window_width / original_width
            if width_ratio < height_ratio
            else (window_height - 120) / original_height
        )

        overlay.controls.clear()
        for astre in astres:
            x, y, width, height = astre["coords"]
            scaled_x = x * (scale_factor - 0.012)
            scaled_y = y * (scale_factor - 0.012)
            scaled_width = width * scale_factor
            scaled_height = height * scale_factor

            border_color = "blue" if astre["name"] in click_order else "grey"

            overlay.controls.append(
                ft.Container(
                    left=scaled_x,
                    top=scaled_y,
                    width=scaled_width,
                    height=scaled_height,
                    data=astre["name"],
                    on_click=on_click,
                    bgcolor=None,
                    border=ft.border.all(2, border_color),
                    border_radius=10,
                )
            )

        page.update()

    astres = [
        {"name": "Neptune", "coords": (140, 730, 450, 140)},
        {"name": "Mars", "coords": (850, 600, 280, 120)},
        {"name": "Saturne", "coords": (1440, 440, 415, 125)},
        {"name": "Lune", "coords": (1110, 350, 175, 90)},
        {"name": "Mercure", "coords": (720, 375, 335, 105)},
        {"name": "Uranus", "coords": (1190, 100, 300, 100)},
        {"name": "Soleil", "coords": (840, 210, 240, 95)},
        {"name": "Vénus", "coords": (790, 0, 270, 90)},
        {"name": "Jupiter", "coords": (250, 110, 380, 120)},
    ]

    solar_system_image = ft.Image(
        src="Vo-D-Solar-system.png",
        fit=ft.ImageFit.CONTAIN,
    )

    overlay = ft.Stack([], expand=True)

    order_label = ft.Text(value="", size=16)

    reset_button = ft.IconButton(
        icon=ft.Icons.RESTART_ALT,
        tooltip="Reset Selection",
        icon_size=24,
        on_click=reset_selection,
    )

    reset_row = ft.Row(
        [reset_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    main_container = ft.Stack([solar_system_image, overlay], expand=True)

    def on_resized(_):
        update_positions()

    page.on_resized = on_resized
    on_resized(None)

    page.add(main_container, order_label, reset_row)


ft.app(target=main)
