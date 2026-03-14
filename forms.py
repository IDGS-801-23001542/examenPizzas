from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class PedidoForm(FlaskForm):
    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es requerido"),
            Length(min=3, max=100, message="Ingrese un nombre válido")
        ]
    )

    direccion = StringField(
        "Dirección",
        validators=[
            DataRequired(message="La dirección es requerida"),
            Length(min=5, max=200, message="Ingrese una dirección válida")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es requerido"),
            Length(min=7, max=20, message="Ingrese un teléfono válido")
        ]
    )

    dia = SelectField(
        "Día",
        choices=[("", "Seleccione día")] + [(str(i), str(i)) for i in range(1, 32)],
        validators=[Optional()]
    )

    mes = SelectField(
        "Mes",
        choices=[
            ("", "Seleccione mes"),
            ("1", "Enero"), ("2", "Febrero"), ("3", "Marzo"), ("4", "Abril"),
            ("5", "Mayo"), ("6", "Junio"), ("7", "Julio"), ("8", "Agosto"),
            ("9", "Septiembre"), ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre")
        ],
        validators=[Optional()]
    )

    anio = SelectField(
        "Año",
        choices=[("", "Seleccione año")] + [(str(i), str(i)) for i in range(2024, 2031)],
        validators=[Optional()]
    )

    tamano = StringField(
        "Tamaño",
        validators=[Optional()]
    )

    numero_pizzas = IntegerField(
        "Número de pizzas",
        validators=[
            Optional(),
            NumberRange(min=1, max=100, message="Cantidad inválida")
        ]
    )

    ingredientes = SelectMultipleField(
        "Ingredientes",
        choices=[
            ("Jamón", "Jamón $10"),
            ("Piña", "Piña $10"),
            ("Champiñones", "Champiñones $10")
        ],
        validators=[Optional()]
    )


class ConsultaDiaForm(FlaskForm):
    dia_semana = SelectField(
        "Día de la semana",
        choices=[
            ("", "Seleccione día"),
            ("0", "Lunes"),
            ("1", "Martes"),
            ("2", "Miércoles"),
            ("3", "Jueves"),
            ("4", "Viernes"),
            ("5", "Sábado"),
            ("6", "Domingo"),
        ],
        validators=[Optional()]
    )

    mes = SelectField(
        "Mes",
        choices=[
            ("", "Seleccione mes"),
            ("1", "Enero"), ("2", "Febrero"), ("3", "Marzo"), ("4", "Abril"),
            ("5", "Mayo"), ("6", "Junio"), ("7", "Julio"), ("8", "Agosto"),
            ("9", "Septiembre"), ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre")
        ],
        validators=[Optional()]
    )

    anio = SelectField(
        "Año",
        choices=[("", "Seleccione año")] + [(str(i), str(i)) for i in range(2024, 2031)],
        validators=[Optional()]
    )


class ConsultaMesForm(FlaskForm):
    mes = SelectField(
        "Mes",
        choices=[
            ("", "Seleccione mes"),
            ("1", "Enero"), ("2", "Febrero"), ("3", "Marzo"), ("4", "Abril"),
            ("5", "Mayo"), ("6", "Junio"), ("7", "Julio"), ("8", "Agosto"),
            ("9", "Septiembre"), ("10", "Octubre"), ("11", "Noviembre"), ("12", "Diciembre")
        ],
        validators=[Optional()]
    )

    anio = SelectField(
        "Año",
        choices=[("", "Seleccione año")] + [(str(i), str(i)) for i in range(2024, 2031)],
        validators=[Optional()]
    )