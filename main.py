import flet as ft

COLOR_APAGADO = "#1A1D24"
BORDER_COLOR = "#333A48"

PALETA = [
    ("#00FF66", "Verde Neón"),
    ("#FFD700", "Amarillo"),
    ("#00E5FF", "Cyan"),
    ("#FF2A6D", "Rojo Neón"),
    ("#BD00FF", "Morado"),
    ("#FFFFFF", "Blanco"),
]

def main(page: ft.Page):
    page.title = "Editor de Sprites 8x8"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 560
    page.window.height = 800
    page.window.resizable = False

    color_pincel = [PALETA[0][0]]
    pixels = []

    def actualizar_hex_desde_matriz():
        cadena_binaria = ""
        for btn in pixels:
            if btn.bgcolor != COLOR_APAGADO:
                cadena_binaria += "1"
            else:
                cadena_binaria += "0"
        
        val_int = int(cadena_binaria, 2)
        val_hex = f"{val_int:016X}"
        lbl_hex.value = f"0x{val_hex}"
        page.update()

    def pixel_click(e):
        btn = e.control
        if btn.bgcolor == COLOR_APAGADO:
            btn.bgcolor = color_pincel[0]
        else:
            btn.bgcolor = COLOR_APAGADO
        actualizar_hex_desde_matriz()

    def seleccionar_color(e):
        color_pincel[0] = e.control.data
        for c in contenedor_paleta.controls:
            c.border = ft.Border.all(3, ft.Colors.WHITE if c.data == color_pincel[0] else ft.Colors.TRANSPARENT)
        page.update()

    grid_matrix = ft.Column(spacing=2)

    row_header = ft.Row(
        spacing=2,
        controls=[ft.Container(width=24)] + [
            ft.Container(
                content=ft.Text(str(col), size=12, color=ft.Colors.GREY, weight=ft.FontWeight.BOLD),
                width=40,
                alignment=ft.Alignment(0, 0)
            ) for col in range(8)
        ]
    )
    grid_matrix.controls.append(row_header)

    for r in range(8):
        row_controls = [
            ft.Container(
                content=ft.Text(str(r), size=12, color=ft.Colors.GREY, weight=ft.FontWeight.BOLD),
                width=24,
                alignment=ft.Alignment(0, 0)
            )
        ]
        for c in range(8):
            btn = ft.Container(
                width=40,
                height=40,
                bgcolor=COLOR_APAGADO,
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=4,
                on_click=pixel_click,
            )
            pixels.append(btn)
            row_controls.append(btn)
        
        grid_matrix.controls.append(ft.Row(controls=row_controls, spacing=2))

    contenedor_paleta = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            ft.Container(
                width=32,
                height=32,
                bgcolor=hex_code,
                border_radius=16,
                data=hex_code,
                on_click=seleccionar_color,
                tooltip=nombre,
                border=ft.Border.all(3, ft.Colors.WHITE if idx == 0 else ft.Colors.TRANSPARENT)
            ) for idx, (hex_code, nombre) in enumerate(PALETA)
        ]
    )

    lbl_hex = ft.Text(
        value="0x0000000000000000",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_ACCENT_200,
    )

    txt_hex_input = ft.TextField(
        label="Código Hexadecimal (16 caracteres)",
        hint_text="Ej: FFFF0000FFFF0000",
        max_length=16,
        width=240,
    )

    def cargar_hex(e):
        input_val = txt_hex_input.value.strip()
        if not input_val:
            return
        try:
            val_int = int(input_val, 16)
            cadena_binaria = f"{val_int:064b}"[-64:].zfill(64)
            for i in range(64):
                if cadena_binaria[i] == "1":
                    pixels[i].bgcolor = color_pincel[0]
                else:
                    pixels[i].bgcolor = COLOR_APAGADO
            actualizar_hex_desde_matriz()
            txt_hex_input.error_text = None
        except ValueError:
            txt_hex_input.error_text = "Hex no válido"
            page.update()

    def limpiar_matriz(e):
        for btn in pixels:
            btn.bgcolor = COLOR_APAGADO
        actualizar_hex_desde_matriz()
        txt_hex_input.value = ""
        txt_hex_input.error_text = None

    def invertir_matriz(e):
        for btn in pixels:
            if btn.bgcolor == COLOR_APAGADO:
                btn.bgcolor = color_pincel[0]
            else:
                btn.bgcolor = COLOR_APAGADO
        actualizar_hex_desde_matriz()

    btn_cargar = ft.ElevatedButton("Cargar Hex", on_click=cargar_hex)
    btn_invertir = ft.OutlinedButton("Invertir", on_click=invertir_matriz)
    btn_limpiar = ft.OutlinedButton("Limpiar", on_click=limpiar_matriz)

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Editor de Sprites 8x8", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona un color para dibujar:", size=12, color=ft.Colors.GREY),
                contenedor_paleta,
                ft.Container(height=10),
                grid_matrix,
                ft.Divider(),
                lbl_hex,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[txt_hex_input, btn_cargar],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[btn_invertir, btn_limpiar],
                ),
            ],
        )
    )

ft.run(main)