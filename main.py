import flet as ft
from flet_navigator import VirtualFletNavigator, PageData, ROUTE_404, route

from tinydb import TinyDB, Query, where
from tinydb.operations import set
db = TinyDB('db.json')

@route('/')
def home(pg: PageData):
    pg.add(ft.Text("Home Page"))
    pg.add(ft.FilledButton(text="Add runner", on_click=lambda _: pg.navigator.navigate('runner_new', pg.page)))
    pg.add(ft.FilledButton(text = "Record Time", on_click= lambda _: pg.navigator.navigate('record_time', pg.page)))

@route("runner_new")
def new_runner(pg: PageData):
    def onUpdateBibNumber(e):
        try:
            int(bib_number_text_box.value)
            bib_number_text_box.error_text = ""
            bibNumber = bib_number_text_box.value
            return bibNumber
        except:
            bib_number_text_box.error_text = "Must be int"
            
    name_text_box = ft.TextField(label="Name")
    bib_number_text_box = ft.TextField(label="Bib Number", on_change= onUpdateBibNumber)


    pg.add( bib_number_text_box, name_text_box)
    def button_clicked(e):
        db.insert({"bib_number" : bib_number_text_box.value, "Name" : name_text_box.value, "Age" : age_dropdown.value, "Gender" : gender_dropdown.value})
        bib_number_text_box.value = ""
        name_text_box.value = ""
        age_dropdown.value = ""
        gender_dropdown.value = ""
        #pg.page.update()
        


    text = ft.Text()
    submit_button = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    
    age_dropdown = ft.Dropdown(
        label= "Age",
        width=100,
        options=[
            ft.dropdown.Option("18-29"),
            ft.dropdown.Option("30-35"),
            ft.dropdown.Option("36-40"),
            ft.dropdown.Option("41-45"),
            ft.dropdown.Option("46-50"),
            ft.dropdown.Option("51-60"),
            ft.dropdown.Option("61-70"),
            ft.dropdown.Option("71+")
        ],
    )

    gender_dropdown = ft.Dropdown(
        label= "Gender",
        width=100,
        options=[
            ft.dropdown.Option("Male"),
            ft.dropdown.Option("Female"),
            ft.dropdown.Option("Other")
        ],
    )
    pg.add(age_dropdown, gender_dropdown, submit_button, text)
     
@route ("record_time")
def record_time(pg: PageData):
    def button_clicked(e):
        a = db.get(where('Bib number')== BibNumber_textbox.value)
        print(a)
        if a == None:
            pg.page.add(text = ft.Text("Bib Number not found"))
        else:
            db.update(where('Bib number') == BibNumber_textbox.value, set('Time', Time_textbox.value))


    BibNumber_textbox =ft.TextField(label= "Bib Number")
    Time_textbox = ft.TextField(label = "Time")
    Submit_button = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    pg.page.add(BibNumber_textbox, Time_textbox, Submit_button)

       
def main(page: ft.Page):
    VirtualFletNavigator().render(page)

ft.app(main)
