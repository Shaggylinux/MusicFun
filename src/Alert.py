import flet   as ft
import Config as co

class Alerta:
    @staticmethod
    def alerta(page: ft.Page, modal: bool, title: str, content: str):
        def cerrar_alerta(e):
            ft.Page.pop_dialog(page)
            page.update()
            
        return ft.AlertDialog(
            modal   = modal,
            title   = ft.Text(title),
            content = ft.Text(content),
            actions = ft.TextButton("Ok", on_click = cerrar_alerta),
            actions_alignment = ft.MainAxisAlignment.END,
        )
    
    @staticmethod
    def update(self : ft.Page, modal : bool):
        def cambiar(e):
            co.editar("Aceptar", 1)
            ft.Page.pop_dialog(self)
            self.update()
        
        return ft.AlertDialog (
            modal   = modal,
            title   = ft.Text(f"Version : {co.leer("Version")}"),
            content = ft.Text("\n".join(co.leer("Changelog"))),
            actions = [ ft.TextButton("Ok",  on_click = cambiar) ],
            actions_alignment = ft.MainAxisAlignment.END
        )