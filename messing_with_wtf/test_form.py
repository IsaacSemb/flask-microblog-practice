from wtforms import Form, StringField, IntegerField, validators

class PersonForm(Form):
    name = StringField(
        label='name', 
        validators=[validators.InputRequired(message="Name is Required")] 
        )
    age = IntegerField(
        label="Age",
        validators=[
            validators.NumberRange(min=18, message="Must be adult"),
            validators.InputRequired(message="Age is Required and must be above 18 years!")
            ]
    )
    
# simulating input
data = [
    
    # correct data 
    {
    "name":"Ssembuusi",
    "age":28
    },
    # missing fields
    {
    "name":"",
    "age":""
    },
    # missing name
    {
    "name":"",
    "age":28
    },
    # under age
    {
    "name":"Ssembuusi",
    "age":16
    },
    # wrong age format
    {
    "name":"Ssembuusi",
    "age":"abc"
    }
]

def show_validity(data, validator_form = PersonForm):
    form = validator_form(data=data)
    
    if form.validate():
        print()
        print("VALID:", form.name.data, form.age.data)
        print("VALID:", form.name, form.age)
        print()
    else:
        print("INVALID:", form.errors)
        

for item_data in data:
    show_validity(data=item_data) 
    
