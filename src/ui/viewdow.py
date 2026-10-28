import os
import flet as ft
import flet_video as ftv
from config import DESCARGAS_DIR

# Formatos que la app reproduce tal cual, sin convertirlos.
# La idea es escuchar/ver el archivo exactamente como lo descargó yt-dlp.
EXT_VIDEO = {".mp4", ".mkv", ".mov", ".avi", ".webm"}
EXT_AUDIO = {".m4a", ".mp3", ".ogg", ".wav", ".flac"}
EXT_REPRODUCIBLES = EXT_VIDEO | EXT_AUDIO

ALTURA_REPRODUCTOR = 240


class Download:

    def __init__(self, page: ft.Page):
        self.page = page
        self.lista = None
        self.panel = None        # contenedor del reproductor (oculto al inicio)
        self.zona_video = None   # donde vive el ft.Video actual
        self.lbl_archivo = None  # nombre del archivo que se está reproduciendo

    # ------------------------------------------------------------------
    # CARPETA
    # ------------------------------------------------------------------
    def _leer_carpeta(self) -> list:
        if not os.path.isdir(DESCARGAS_DIR):
            return []
        return sorted(os.listdir(DESCARGAS_DIR))

    def _ruta(self, nombre: str) -> str:
        return os.path.join(DESCARGAS_DIR, nombre)

    # ------------------------------------------------------------------
    # REPRODUCCIÓN
    # ------------------------------------------------------------------
    def _reproducir(self, nombre: str):
        """Carga el archivo en el reproductor (abajo de la ventana)."""
        ruta = self._ruta(nombre)
        if not os.path.isfile(ruta):
            return

        # Un solo reproductor a la vez: el control anterior se retira
        # (y al retirarse deja de sonar).
        self._detener_reproductor()

        self.lbl_archivo.value = nombre
        self.zona_video.content = ftv.Video(
            height=ALTURA_REPRODUCTOR,
            autoplay=True,
            playlist=[ftv.VideoMedia(ruta)],
        )
        self.panel.visible = True
        self.page.update()

    def _detener_reproductor(self):
        # Retirar el control basta: al desmontarse, el reproductor se cierra
        # y deja de sonar. (No hay que llamar a stop(): el control ya no está
        # en pantalla y eso tumba la sesión.)
        self.zona_video.content = None

    def _cerrar(self, e):
        self._detener_reproductor()
        self.lbl_archivo.value = ""
        self.panel.visible = False
        self.page.update()

    def _abrir_carpeta(self, nombre: str):
        ruta = self._ruta(nombre)
        if os.path.isdir(ruta):
            os.startfile(ruta)  # abre la carpeta en el Explorador de Windows

    # ------------------------------------------------------------------
    # INTERFAZ: convertir cada archivo en una fila visual
    # ------------------------------------------------------------------
    def _crear_items(self) -> list:
        """Crea una fila (ListTile) por cada archivo o carpeta encontrada."""
        items = []

        for nombre in self._leer_carpeta():
            es_carpeta = os.path.isdir(self._ruta(nombre))
            ext = os.path.splitext(nombre)[1].lower()
            reproducible = (not es_carpeta) and ext in EXT_REPRODUCIBLES

            if es_carpeta:
                icono = ft.Icons.FOLDER
                detalle = "Carpeta"
                # Clic en la carpeta: la abre en el Explorador.
                accion = ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN,
                    tooltip="Abrir carpeta",
                    on_click=lambda e, n=nombre: self._abrir_carpeta(n),
                )
            else:
                if ext in EXT_AUDIO:
                    icono = ft.Icons.MUSIC_NOTE
                elif ext in EXT_VIDEO:
                    icono = ft.Icons.MOVIE
                else:
                    icono = ft.Icons.DESCRIPTION
                detalle = ext.upper()

                # Archivo reproducible: botón de reproducción.
                accion = (
                    ft.IconButton(
                        icon=ft.Icons.PLAY_ARROW,
                        tooltip="Reproducir",
                        on_click=lambda e, n=nombre: self._reproducir(n),
                    )
                    if reproducible
                    else None
                )

            items.append(
                ft.ListTile(
                    leading=ft.Icon(icono),
                    title=ft.Text(nombre),
                    subtitle=ft.Text(detalle),
                    trailing=accion,
                )
            )

        # Aviso amable si la carpeta está vacía
        if not items:
            items.append(
                ft.ListTile(title=ft.Text("La carpeta de descargas está vacía"))
            )

        return items

    def _actualizar(self, e=None):
        self.lista.controls = self._crear_items()
        self.page.update()

    def build_player(self) -> ft.Control:
        """Panel con el reproductor: se muestra abajo del todo y solo cuando
        se reproduce algo (si está oculto no ocupa espacio)."""
        self.lbl_archivo = ft.Text(
            "",
            size=13,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.PURPLE_700,
        )
        self.zona_video = ft.Container(height=ALTURA_REPRODUCTOR)

        self.panel = ft.Container(
            visible=False,
            padding=12,
            border_radius=12,
            bgcolor=ft.Colors.PURPLE_50,
            border=ft.Border.all(1, ft.Colors.PURPLE_200),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PLAY_CIRCLE_FILL,
                                        color=ft.Colors.PURPLE_600,
                                    ),
                                    self.lbl_archivo,
                                ],
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Cerrar reproductor",
                                on_click=self._cerrar,
                            ),
                        ],
                    ),
                    self.zona_video,
                ],
            ),
        )
        return self.panel

    def build_download(self) -> ft.Control:
        self.lista = ft.ListView(controls=self._crear_items(), expand=True)

        return ft.Column(
            expand=True,
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Actualizar lista",
                            on_click=self._actualizar,
                        )
                    ],
                ),
                self.lista,
            ],
        )
