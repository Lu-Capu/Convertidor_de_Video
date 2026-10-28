import flet as ft
from ui.downloader import Downloader
from ui.viewdow import Download  # pestaña "Mis Descargas"


class Principal:

    def __init__(self, page: ft.Page):
        self.page = page
        self.down = Downloader()
        self.vista_descargas = Download(page)  # vista de la pestaña "Mis Descargas"

        self.lbl_titulo = ft.Text(
            "Descargador Multimedia",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.PURPLE_700,
        )
        self.lbl_sub_titulo = ft.Text(
            "Obtén videos en MP4 en alta calidad directamente a tu carpeta local.",
            size=12,
            color=ft.Colors.PURPLE_500,
        )
        self.txt_url = ft.TextField(
            label="URL del video de YouTube",
            hint_text="https://www.youtube.com/watch?v=...",
            prefix_icon="link",
            on_submit=self._on_descargar,
        )
        self.combo_box = ft.Dropdown(
            label="Elige un formato de descarga",
            hint_text="Selecciona una opción",
            width=300,
            value="1",
            options=[
                ft.dropdown.Option("1", "Video (MP4)"),
                ft.dropdown.Option("2", "Audio Nativo (M4A/WebM)"),
            ],
            on_select=self.opcion_cambiada,
        )
        self.btn_descargar = ft.Button(
            "Descargar",
            icon=ft.icons.Icons.DOWNLOAD,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.PURPLE_600),
            on_click=self._on_descargar,
        )
        self.valor = 1
        self.progreso = ft.ProgressBar(color=ft.Colors.PURPLE_600, visible=False)
        self.lbl_estado = ft.Text("", selectable=True)

    def opcion_cambiada(self, e):
        valor_seleccionado = e.control.value
        if not valor_seleccionado:
            return

        try:

            self.valor = int(valor_seleccionado)
            self.lbl_estado.value = f"Opción seleccionada: {self.valor}"
            self.lbl_estado.color = None
        except ValueError:
            self.lbl_estado.value = "Hubo un error al procesar la opción"
            self.lbl_estado.color = ft.Colors.ORANGE

        self.page.update() 
    
    def _on_descargar(self, e):
        if self.btn_descargar.disabled:
            return

        url = (self.txt_url.value or "").strip()
        if not url:
            self.lbl_estado.value = "Pega un link primero."
            self.lbl_estado.color = ft.Colors.ORANGE
            self.page.update()
            return

        self.btn_descargar.disabled = True
        self.txt_url.disabled = True
        self.progreso.visible = True
        self.lbl_estado.value = "Descargando..."
        self.lbl_estado.color = None
        self.page.update()

        # En un hilo para no congelar la interfaz
        self.page.run_thread(self._descargar, url)

    def _descargar(self, url: str):
        ok, mensaje = self.down.descargar_video(self.valor, url)
        self.lbl_estado.value = mensaje
        self.lbl_estado.color = ft.Colors.GREEN if ok else ft.Colors.RED
        self.btn_descargar.disabled = False
        self.txt_url.disabled = False
        self.progreso.visible = False
        self.page.update()

    def _create_tarjeta(self):
        return ft.Container(
            width=500,
            padding=20,
            border_radius=12,
            bgcolor=ft.Colors.PURPLE_50,
            border=ft.Border.all(1, ft.Colors.PURPLE_200),
            content=ft.Column(
                controls=[
                    self.lbl_titulo,
                    self.lbl_sub_titulo,
                    self.txt_url,
                    self.combo_box,
                    self.btn_descargar,
                    self.progreso,
                    self.lbl_estado,
                ],
                spacing=15,
            ),
        )

    def build_view(self):
        tabs = ft.Tabs(
            length=2,
            selected_index=0,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Descargar"),
                            ft.Tab(label="Mis Descargas"),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            self._create_tarjeta(),
                            # Segunda pestaña: lista todo lo que hay en "descargas"
                            self.vista_descargas.build_download(),
                        ],
                    ),
                ],
            ),
        )
        # El reproductor va fuera de las pestañas (abajo): así sigue sonando
        # aunque cambies de pestaña.
        self.page.add(
            ft.Column(
                expand=True,
                spacing=10,
                controls=[
                    tabs,
                    self.vista_descargas.build_player(),
                ],
            )
        )
