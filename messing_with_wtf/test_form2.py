from wtforms import Form, StringField, IntegerField, validators
from werkzeug.datastructures import MultiDict

class PersonForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    age = IntegerField('Age', [validators.NumberRange(min=0)])

# Simulate input
# data = {"name": "Isaac", "age": 25}


# Simulate form input using MultiDict
data = MultiDict({"name": "Isaac", "age": "25"})  # age should be string to mimic real form input


form = PersonForm(data=data)

if form.validate():
    print("✅ Valid:", form.name.data, form.age.data)
else:
    print("❌ Errors:", form.errors)
