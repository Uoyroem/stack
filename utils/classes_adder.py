def classes_adder(form, classes: str) -> type:
  for visible in form.visible_fields():
    visible.field.widget.attrs['class'] = classes
        
