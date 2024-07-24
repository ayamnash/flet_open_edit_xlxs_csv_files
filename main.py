import flet as ft
import pyperclip
import math
import pandas as pd
import numpy as np


class NavDraw(ft.NavigationDrawer):
    def __init__(self, page,pick_file_callback):
        self.page = page
        self.pick_file_callback = pick_file_callback
        self.page.drawer = ft.NavigationDrawer(
            on_change=self.on_drawer_change,
            controls=[
                ft.Container(height=12),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                    label="About",
                    selected_icon=ft.icons.INFO,
                ),ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.FILE_OPEN_ROUNDED),
                    label="Pick xlsx or csv files",
                    selected_icon=ft.icons.INFO,
                ),
            ],
        )

    def show_drawer(self, e):
        self.page.drawer.open = True
        self.page.drawer.update()

    def hide_drawer(self, e):
        self.page.drawer.open = False
        self.page.drawer.update()

    def on_drawer_change(self, e):
        if e.control.selected_index == 0:  # "Item 1" is at index 0
            self.naser(e)
        if e.control.selected_index == 1:  # "ayman" is at index 1
            self.pick_file_callback(e)
            self.hide_drawer(e)



    def naser(self, e):
        alert_dialog = diaolog = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Text( "Instructions", size=30, color="pink600", italic=True
                    )

                ]

            ),

            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                        ft.Divider(),

                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.ADD,
                                        icon_size=15,
                                         icon_color=ft.colors.BLUE,
                                        bgcolor=ft.colors.YELLOW_200,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='using to open csv or xlsx files',
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),
                            ft.Divider(),

                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.SAVE,
                                        icon_size=15,
                                        bgcolor=ft.colors.YELLOW_200,
                                        icon_color=ft.colors.BLUE,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='using to save files \nafter editing as csv extension',
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),ft.Divider(),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.CODE,
                                        icon_size=15,
                                        bgcolor=ft.colors.YELLOW_200,
                                        icon_color=ft.colors.BLUE,
                                        
                                        
                                    ),
                                    ft.Text(
                                value='using to write\n Pandas commands\n for the picked file\n and run it',
                                color=ft.colors.BLACK,
                                size=15
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),ft.Divider(),

                            ft.Row(controls=[
                            ft.TextField(
                               border_radius=40,
                               hint_text='input your search',
                               text_size=15,
                                color=ft.colors.WHITE,
                                hint_style=ft.TextStyle(color=ft.colors.WHITE),
                                text_vertical_align=1,
                                width=40,
                                height=20,
                                prefix_icon=ft.icons.SEARCH,
    
                                ),
                            ft.Text(
                                value='using to search \n and  filter result',
                                color=ft.colors.BLACK,
                                size=15
                            ),

                            ]),ft.Divider(),

                            
                            ft.TextButton(
                                'To contact the developer \ntelegram ',
                                on_click=self.open_link,icon="TELEGRAM",
                                 icon_color="green400",
                                style=ft.ButtonStyle(
            color=ft.colors.BLUE,  # Set the text color here
        ),
                               
                            )
                            ,

                            
                           
                            
                        ],
                        
                    
                        
                    )
                ],
                
                horizontal_alignment='start'
                
            )
        
        ,


            actions=[ft.TextButton(text="Close", on_click=self.close_dialog)],
            open=True,
            
        )
        self.page.overlay.append(alert_dialog)
        alert_dialog.open = True
        self.page.update()
        
        # self.page.dialog = diaolog 
        # self.page.update() 
        # self.page.dialog = alert_dialog
        # alert_dialog.open = True
        # self.page.update()
    def close_dialog(self, e):
        if self.page.overlay and len(self.page.overlay) > 0:
            dialog = self.page.overlay.pop()
            if isinstance(dialog, ft.AlertDialog):
                dialog.open = False
        self.page.update()
    def open_link(self,e):
        self.page.launch_url("https://t.me/ayamnash")    

    


df = None  # Define df as a global variable
filtered_df = None  # Define filtered_df as a global variable
current_page = 0  # Keep track of the current page

def load_data(file_path: str) -> pd.DataFrame:
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding=encoding)
                return df
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                return df
            else:
                raise ValueError("Unsupported file format")
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode file with tried encodings: {encodings}")

def headers(df: pd.DataFrame) -> list:
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]

def rows(df: pd.DataFrame, on_row_click, start_index: int, end_index: int) -> list:
    rows = []
    for index, row in df.iloc[start_index:end_index].iterrows():
        cells = [ft.DataCell(ft.Text(str(row[header]))) for header in df.columns]
        data_row = ft.DataRow(
            cells=cells,
            on_select_changed=lambda e, idx=index: on_row_click(idx) if e.data else None
        )
        rows.append(data_row)
    return rows

def update_datatable(page: ft.Page, datatable: ft.DataTable, on_row_click, filtered_df=None):
    global df, current_page
    if filtered_df is None:
        filtered_df = df
    total_pages = math.ceil(len(filtered_df) / 10)
    start_index = current_page * 10
    end_index = start_index + 10
    datatable.columns = headers(filtered_df)
    
    datatable.rows = rows(filtered_df, on_row_click, start_index, end_index)
    page.update()

def create_sum_container():
    global df  # Ensure df is accessible in this scope
    if df is not None:
        numeric_sums = df.sum(numeric_only=True).round(3)
        tite = ft.Row(controls=[ft.Text('Sum for columns that contain numbers',color=ft.colors.BLACK)])

       
        header_row = ft.Row([ft.Text(f"{header}/", color=ft.colors.WHITE) for header in numeric_sums.index])
        sum_row = ft.Row([ft.Text(f"{value}/", color=ft.colors.WHITE) for value in numeric_sums.values])
        

        return ft.Container(
            content=ft.Column([tite,header_row, sum_row], auto_scroll=True, scroll=True),
            padding=ft.padding.all(10),
            bgcolor=ft.colors.BLUE,

        )
    else:
        return ft.Text("No data loaded yet. Please load a CSV or XLSX file first.")

def update_sum_container(page, sum_container):
    sum_container.content = create_sum_container()
    page.update()
def update_info_text(page: ft.Page, total_rows: int, total_pages: int,current_page:int='1'):
    # Access the existing info_text widget (assuming it's a global variable)
    global info_text

    info_text.value = f"Rows: {total_rows} | Pages: {total_pages} | current_page: {current_page}"
    page.update()  # Trigger a UI refresh
def main(page: ft.Page):

    theme = page.client_storage.get('theme')
    if theme is None:
        theme = ft.ThemeMode.LIGHT.value
        page.client_storage.set('theme', theme)
    
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    page.window.width = 1100
    page.window.height = 900
    page.window.center()
    page.theme_mode = theme
    page.window.maximizable = True
    
    global df, filtered_df, current_page ,info_text # Ensure global variables are accessible in this scope

    datatable = datatable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("")),
            
          
        ]
    )
    sum_container = ft.Container()
    def toggle_theme(e):
        if page.theme_mode == "dark":
            page.theme_mode = "light"
           
        else:
            page.theme_mode = "dark"
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        global df, filtered_df, current_page
        if e.files:
            file_path = e.files[0].path
            df = load_data(file_path)
            filtered_df = df.copy()  # Initialize filtered_df
            current_page = 0  # Reset to the first page

            # Check the number of rows and set container visibility
            if len(df) < 11:
                container.visible = False
            else:
                container.visible = True

            update_datatable(page, datatable, on_row_click)
            add_row_button.visible = True
            save_button.visible = True
            run_button.visible = True
            #sum_numeric_button.visible=True
            total_rows = len(df)
            page_size = 10  # Assuming 10 rows per page
            total_pages = math.ceil(total_rows / page_size)

            # Update the info text widget
            update_info_text(page, total_rows, total_pages)
            update_sum_container(page, sum_container)
            page.update()
    
    def on_save_as_result(e: ft.FilePickerResultEvent):
        global df  # Ensure df is accessible in this scope
        if e.path:
            try:
                file_path = e.path
                df.to_csv(file_path, index=False)
                page.snack_bar = ft.SnackBar(ft.Text("Data saved successfully!"))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error saving file: {ex}"))
                page.snack_bar.open = True
                page.update()


    file_picker = ft.FilePicker(on_result=on_file_picked)
    save_picker = ft.FilePicker(on_result=on_save_as_result)
    page.overlay.append(file_picker)
    page.overlay.append(save_picker)

    def pick_file(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=['csv', 'xlsx'])
        #e.control.color='green'
        #e.control.update()

    pick_file_button = ft.ElevatedButton(text="pick csv~xlsx ", bgcolor="blue",color="white", icon=ft.icons.FILE_OPEN_ROUNDED, icon_color=ft.colors.BLUE_100, on_click=pick_file)

    def update_cell_value(row_index, column_index, value):
        global df  # Ensure df is accessible in this scope
        df.iloc[row_index, column_index] = value
        update_datatable(page, datatable, on_row_click)

    def add_row():
        global df, filtered_df  # Ensure df and filtered_df are accessible in this scope
        new_row = pd.DataFrame({column: [""] for column in df.columns}, index=[len(df)])
        df = pd.concat([df, new_row], ignore_index=True)
        filtered_df = df.copy()  # Update filtered_df as well
        update_datatable(page, datatable, on_row_click)
        last_page(None)  # Navigate to the last page
        on_row_click(len(df) - 1)  # Open the AlertDialog for the new row


    def save_changes(e):
        save_picker.save_file(file_name="data.csv", allowed_extensions=['csv'])

      
    def ppp(e):
        result_datatable = datatable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("")),
            
            # Add more columns as needed
        ]
    )
        
        def close_dialog(e):
            command_dialog.open = False
            page.update()
       
        def run_command(e):
            try:
                command = command_input.value
                # Split the command into lines
                lines = command.splitlines()
                
                # Dictionary to hold local variables
                local_vars = {}
                
                # Execute all but the last line using exec() and store the local variables
                for line in lines[:-1]:
                    exec(line, globals(), local_vars)
                
                # Evaluate the last line using eval() if it's an expression or exec() if it's a statement
                try:
                    result = eval(lines[-1], globals(), local_vars)
                except SyntaxError:
                    exec(lines[-1], globals(), local_vars)
                    result = None

                # If the result is a DataFrame, display it using your existing logic
                if isinstance(result, pd.DataFrame):
                    result_datatable.columns = headers(result)
                    result_datatable.rows = rows(result, lambda idx: None, 0, len(result))
                    result_container.content = result_datatable
                elif result is not None:
                    result_container.content = ft.Text(f"Result: {result}")
                else:
                    result_container.content = ft.Text("Command executed successfully.")

            except Exception as ex:
                result_container.content = ft.Text(f"Error: {ex}")

            page.update()



        
        def coppy(e):
            if isinstance(result_container.content, ft.DataTable):
                # Get the headers of the DataTable
                headers = result_container.content.columns
                headers_text = '\t'.join([header.label.value for header in headers])

                # Get the text representation of the DataTable rows
                rows_text = '\n'.join(['\t'.join([cell.content.value for cell in row.cells]) for row in result_container.content.rows])

                # Combine headers and rows
                table_text = f"{headers_text}\n{rows_text}"

                # Copy the table text to the clipboard
                pyperclip.copy(table_text)

    
            else:
                # If the content is not a DataTable, copy the text as is
                pyperclip.copy(str(result_container.content))
        def opcao_escolhida(e):
            
            command_input.value = e.control.value
            page.update()
        command_input = ft.TextField(label="Input Pandas command",multiline=True, hint_text="df.sum(numeric_only=True)")
        cop=ft.IconButton(
                                            icon=ft.icons.CONTENT_COPY,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.YELLOW_200,
                                            opacity=0.9,
                                            width=60,
                                            height=40,
                                            alignment=ft.alignment.center,
                                            on_click=coppy,
                                        )
        drp = ft.ResponsiveRow(
        controls=[
            ft.Column(
                col={'sm': 12},
                controls=[
                    ft.Dropdown(
                        label=' most common  commands',
                        label_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        options=[
                            ft.dropdown.Option(text="#using numpy library \nsum_marks = np.sum(df['col_name'])\nsum_marks"),
                            ft.dropdown.Option(text="sorted_df = df.sort_values(by='col_name', ascending=True)\ntop_five = sorted_df.head(4)\ntop_five"), 
                            ft.dropdown.Option(text="df.head()"),
                            ft.dropdown.Option(text="df.groupby(['col_name'])['col_number_name'].sum()"),
                            ft.dropdown.Option(text="df['col_name'].describe()"),
                            ft.dropdown.Option(text="df.sum(numeric_only=True)"),
                            ft.dropdown.Option(text="df.columns"),
                            ft.dropdown.Option(text="df['col_name'].head(5)"),
                            ft.dropdown.Option(text="df.drop('col_name', axis=1)"),
                            ft.dropdown.Option(text="df['New Column'] = 0"),
                            ft.dropdown.Option(text="df.sort_values(by=['Population'], ascending=False)"),
                            ft.dropdown.Option(text="df.rank()"),
                            ft.dropdown.Option(text="df.columns"),
                            ft.dropdown.Option(text="df.drop('col_name', axis=1)"),
                            ft.dropdown.Option(text="df.max()"),
                            ft.dropdown.Option(text="df.min()"),
                        ],
                        on_change=opcao_escolhida
                    )
                ]
            )
        ]
    )
        close_d=ft.TextButton("Close", on_click=close_dialog)
        run_button = ft.ElevatedButton(text="Run", on_click=run_command)
        result_container = ft.Container()
        def opcao_escolhida(e):
            command_input.value = e.control.value
            page.update()
        drow=ft.Row([run_button,close_d])
        dialog_content = ft.Column([cop,drp,command_input,drow,ft.Row([result_container],scroll= ft.ScrollMode.ALWAYS)] ,scroll= ft.ScrollMode.ALWAYS)
        command_dialog = ft.AlertDialog(title=ft.Text("Run Pandas Command"), content=dialog_content)
        page.overlay.append(command_dialog)

        command_dialog.open = True
        page.update()



    def on_row_click(row_index):
        global df, filtered_df  # Ensure df and filtered_df are accessible in this scope
        selected_row = df.iloc[row_index]
       
        dialog = ft.AlertDialog(title =ft.Text('Add-Edit'))
       
        


        def update_and_close(e):
            for i, column in enumerate(df.columns):
                new_value = inputs[i].value
                try:
                    # Convert the new value to the original data type
                    original_type = df[column].dtype
                    if pd.api.types.is_numeric_dtype(original_type):
                        new_value = pd.to_numeric(new_value)
                    elif pd.api.types.is_datetime64_any_dtype(original_type):
                        new_value = pd.to_datetime(new_value)
                    # Assign the converted value back to the DataFrame
                    df.at[row_index, column] = new_value
                except Exception as ex:
                    print(f"Error converting value: {ex}")
            filtered_df = df.copy()  # Update filtered_df to reflect changes
            update_datatable(page, datatable, on_row_click)
            dialog.open = False
            total_rows = len(df)
            page_size = 10  # Assuming 10 rows per page
            total_pages = math.ceil(total_rows / page_size)

            # Update the info text widget
            update_info_text(page, total_rows, total_pages)
            update_sum_container(page, sum_container)
            page.update()

        def delete_row(e):
            global df, filtered_df  # Ensure df and filtered_df are accessible in this scope
            df = df.drop(row_index)
            df = df.reset_index(drop=True)
            filtered_df = df.copy()  # Update filtered_df to reflect changes
            update_datatable(page, datatable, on_row_click)
            dialog.open = False
            total_rows = len(df)
            page_size = 10  # Assuming 10 rows per page
            total_pages = math.ceil(total_rows / page_size)

            # Update the info text widget
            update_info_text(page, total_rows, total_pages)
            update_sum_container(page, sum_container)
            page.update()

        inputs = [ft.TextField(label=column, value=str(selected_row[column])) for column in df.columns]
        update_button = ft.ElevatedButton(text="Update", on_click=update_and_close)
        delete_button = ft.ElevatedButton(text="Delete", on_click=delete_row)
        tol = ft.Row(
            controls=[update_button, delete_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Spread buttons evenly across the row
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center buttons vertically
            wrap=True,
            spacing=20,
        )
        dialog.content = ft.Column(inputs + [tol], auto_scroll=False, scroll=True)
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    ND=NavDraw(page, pick_file)
    add_row_button = ft.IconButton(
                                            icon=ft.icons.ADD,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.YELLOW_200,
                                            opacity=0.9,
                                            width=60,
                                            height=40,
                                            alignment=ft.alignment.center, on_click=lambda _: add_row(), visible=False)
    save_button = ft.IconButton(
                                            icon=ft.icons.SAVE,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.YELLOW_200,
                                            opacity=0.9,
                                            width=60,
                                            height=40,
                                            alignment=ft.alignment.center, on_click=save_changes, visible=False)
    
    run_button = ft.IconButton(
                                          icon=ft.icons.CODE,
                                          icon_size=30,
                                          icon_color=ft.colors.BLUE,
                                          bgcolor=ft.colors.YELLOW_200,
                                          opacity=0.9,
                                          width=60,
                                          height=40,
                                          alignment=ft.alignment.center,
                                          on_click=ppp,
                                          visible=False
    )
    def open_snack_bar(page, msg):
        page.snack_bar=ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()
    def change_theme(e):
        """
        切换主题
        """
        if page.theme_mode == ft.ThemeMode.LIGHT.value:
            page.theme_mode = ft.ThemeMode.DARK.value
            open_snack_bar(page, 'dark theme')
        else:
            page.theme_mode = ft.ThemeMode.LIGHT.value
            open_snack_bar(page, 'light theme')
        page.client_storage.set('theme',page.theme_mode)
        page.update()
    def first_page(e):
        global current_page
        current_page = 0
        cur=current_page +1
        total_rows = len(df)
        page_size = 10  # Assuming 10 rows per page
        total_pages = math.ceil(total_rows / page_size)
        update_info_text(page, total_rows, total_pages,cur)
        update_datatable(page, datatable, on_row_click)

    def last_page(e):
        global current_page, filtered_df
        total_pages = math.ceil(len(filtered_df) / 10)
        current_page = total_pages - 1
        cur=current_page +1
        total_rows = len(df)
        page_size = 10  # Assuming 10 rows per page
        total_pages = math.ceil(total_rows / page_size)
        update_info_text(page, total_rows, total_pages,cur)
        update_datatable(page, datatable, on_row_click)
    
    def next_page(e):
        global current_page, filtered_df
        if (current_page + 1) * 10 < len(filtered_df):
            current_page += 1
            cur=current_page +1
            total_rows = len(df)
            page_size = 10  # Assuming 10 rows per page
            total_pages = math.ceil(total_rows / page_size)
            update_info_text(page, total_rows, total_pages,cur)
            update_datatable(page, datatable, on_row_click, filtered_df=filtered_df)

    def prev_page(e):
        global current_page, filtered_df
        if current_page > 0:
            current_page -= 1
            cur=current_page +1
            total_rows = len(df)
            page_size = 10  # Assuming 10 rows per page
            total_pages = math.ceil(total_rows / page_size)
            update_info_text(page, total_rows, total_pages,cur)
            update_datatable(page, datatable, on_row_click, filtered_df=filtered_df)
    def found(e):
        global filtered_df, df, current_page
        search_text = textfield1.value
        loading_indicator.visible = True  # Show the loading indicator
        page.update()
        if search_text:
            # Convert DataFrame to NumPy array
            data_array = df.values
            # Flatten the array
            flat_data = np.ravel(data_array.astype(str))
            # Convert the search text to a NumPy array
            search_array = np.array([search_text] * flat_data.size)
            # Use np.char.find to find the indices where the search text is present
            indices = np.char.find(flat_data, search_array) >= 0
            # Use np.unique to get unique row indices
            row_indices = np.unique(indices.reshape(-1, data_array.shape[1]).any(axis=1).nonzero()[0])
            # Create a new DataFrame with the filtered rows
            filtered_df = df.iloc[row_indices]
        else:
            filtered_df = df
        current_page = 0  # Reset to the first page
        update_datatable(page, datatable, on_row_click, filtered_df=filtered_df)  
        loading_indicator.visible = False  # Hide the loading indicator
        page.update()

    header = ft.Text("Navigate", size=11, weight=ft.FontWeight.BOLD,color=ft.colors.WHITE)
    first_button = ft.IconButton(icon=ft.icons.FIRST_PAGE,icon_color="white", on_click=first_page)
    last_button = ft.IconButton(icon=ft.icons.LAST_PAGE,icon_color="white",on_click=last_page)
    prev_button = ft.IconButton(icon=ft.icons.CHEVRON_LEFT,icon_color="white", on_click=prev_page)
    
    next_button = ft.IconButton(icon=ft.icons.CHEVRON_RIGHT,icon_color="white", on_click=next_page)
    
    loading_indicator = ft.ProgressRing(width=16, height=16, stroke_width = 2,visible=False)
    
    textfield1 = ft.TextField(
        border_radius=40,
        hint_text='input your search',
        text_size=15,
        color=ft.colors.BLACK,
        hint_style=ft.TextStyle(color=ft.colors.WHITE),
        text_vertical_align=1,
        width=335 * 0.82,
        height=40,
        prefix=ft.IconButton(
            icon=ft.icons.SEARCH,
            on_click=found)
        
    )

    navigation_row_1 = ft.Row(
        controls=[pick_file_button, add_row_button, save_button,run_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Spread buttons evenly across the row
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center buttons vertically
        wrap=True,
        spacing=0,

    )

    navigation_row_11 = ft.Container(
        content=navigation_row_1,
        padding=ft.padding.only(top=10, left=5)  # Add padding around the row
    )

    navigation_row_2 = ft.Row(
        controls=[header, last_button, first_button, next_button, prev_button],
    )
    
    n_2 = ft.Row(
        controls=[textfield1,loading_indicator],
    )
    
    container = ft.Container(
        alignment=ft.alignment.center,
        width=350,
        height=100,
        content=ft.Column(
            controls=[
                navigation_row_2, n_2
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(left=10),
        border_radius=10,
        bgcolor=ft.colors.BLUE,
        visible=False  # Set initial visibility to False
    )
    info_text = ft.Text(size=11,width=300,
            height=13,value="")  # Create an empty Text widget initially
    thee = ft.IconButton(
                                            icon=ft.icons.WB_SUNNY_OUTLINED,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.YELLOW_200,
                                            #opacity=0.9,
                                            width=60,
                                            visible=True,
                                            height=40,
                                            alignment=ft.alignment.center, on_click=change_theme)
    ttt = ft.IconButton(
                                            icon=ft.icons.MENU,
                                            icon_size=30,
                                            icon_color=ft.colors.BLUE,
                                            bgcolor=ft.colors.YELLOW_200,
                                            opacity=0.9,
                                            width=60,
                                            height=40,
                                            alignment=ft.alignment.center, on_click=ND.show_drawer)
    par = ft.Row(controls=[ttt,thee,info_text])
    cv = ft.Column([datatable,sum_container], scroll=True)
    rv = ft.Row([cv], scroll=True, expand=1, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(par,navigation_row_11, container, rv)

ft.app(
    
    target=main,
    name="Edit_csv_xlsx_pandas_py",
    assets_dir="assets",
    use_color_emoji=True,
    web_renderer=ft.WebRenderer.CANVAS_KIT,

)
