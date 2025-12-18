from db import main_db
import flet as ft

def main(page: ft.Page):
    page.title = 'ToDO List'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column(spacing=30)

    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed=completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def del_task(_):
            main_db.delete_task(task_id=task_id)
            load_tasks()
            page.update()

        del_button = ft.IconButton(icon=ft.Icons.DELETE,on_click=del_task)

        return ft.Row([checkbox, task_field, edit_button, save_button,del_button])
    
    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()
    
    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))
            print(f'Задача {task} completed - id {task_id}')
            task_input.value = None
            page.update()

    task_input = ft.TextField(label='Введите задачу', on_submit=add_task, expand=True)
    task_input_button = ft.IconButton(icon=ft.Icons.SEND, on_click=add_task)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()
    
    def del_com_tasks(_):
        main_db.del_completed_task()
        load_tasks()
        page.update()

    del_com_tasks = ft.ElevatedButton(text='Удалить выполненные задачи.',on_click=del_com_tasks,icon=ft.Icons.DELETE,icon_color=ft.Colors.RED)

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.YELLOW),
        ft.ElevatedButton('Ожидают', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.WATCH_LATER, icon_color=ft.Colors.RED),
        ft.ElevatedButton("Готово", on_click=lambda e: set_filter('completed'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Row([task_input, task_input_button]), filter_buttons, task_list,del_com_tasks)
    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)