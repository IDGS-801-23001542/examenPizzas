import datetime

from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy import extract

from . import pizzeria
from forms import PedidoForm, ConsultaDiaForm, ConsultaMesForm
from models import db, Cliente, Pizza, Pedido, DetallePedido


PRECIOS = {
    "Chica": 40,
    "Mediana": 80,
    "Grande": 120
}

PRECIO_INGREDIENTE = 10

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}

MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}


def obtener_fecha_hoy():
    return datetime.date.today()


def obtener_detalle():
    if "detalle_pedido" not in session:
        session["detalle_pedido"] = []
    return session["detalle_pedido"]


def obtener_datos_cliente():
    if "datos_cliente" not in session:
        session["datos_cliente"] = {
            "nombre": "",
            "direccion": "",
            "telefono": "",
            "fecha": obtener_fecha_hoy().isoformat()
        }
    else:
        if "fecha" not in session["datos_cliente"]:
            session["datos_cliente"]["fecha"] = obtener_fecha_hoy().isoformat()
            session.modified = True
    return session["datos_cliente"]


def limpiar_sesion_pedido():
    session["detalle_pedido"] = []
    session["datos_cliente"] = {
        "nombre": "",
        "direccion": "",
        "telefono": "",
        "fecha": obtener_fecha_hoy().isoformat()
    }
    session.modified = True


def calcular_precio_unitario(tamano, ingredientes):
    precio_base = PRECIOS.get(tamano, 0)
    extras = len(ingredientes) * PRECIO_INGREDIENTE
    return precio_base + extras


def calcular_total(detalle):
    return sum(float(item["subtotal"]) for item in detalle)


def obtener_ventas_hoy():
    hoy = obtener_fecha_hoy()
    pedidos_hoy = (
        Pedido.query
        .filter(Pedido.fecha == hoy)
        .order_by(Pedido.id_pedido.desc())
        .all()
    )

    total_hoy = sum(float(p.total) for p in pedidos_hoy)
    return pedidos_hoy, total_hoy


def construir_fecha_hoy():
    return obtener_fecha_hoy()


def convertir_fecha_desde_formulario(fecha_texto):
    try:
        return datetime.datetime.strptime(fecha_texto, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def obtener_o_crear_cliente(nombre, direccion, telefono):
    cliente = Cliente.query.filter_by(
        nombre=nombre,
        direccion=direccion,
        telefono=telefono
    ).first()

    if not cliente:
        cliente = Cliente(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        db.session.add(cliente)
        db.session.flush()

    return cliente


def obtener_o_crear_pizza(tamano, ingredientes, precio):
    pizza = Pizza.query.filter_by(
        tamano=tamano,
        ingredientes=ingredientes,
        precio=precio
    ).first()

    if not pizza:
        pizza = Pizza(
            tamano=tamano,
            ingredientes=ingredientes,
            precio=precio
        )
        db.session.add(pizza)
        db.session.flush()

    return pizza


@pizzeria.route("/pizzeria", methods=["GET", "POST"])
@pizzeria.route("/pizzeria/index", methods=["GET", "POST"])
def index():
    form = PedidoForm()
    detalle = obtener_detalle()
    datos_cliente = obtener_datos_cliente()

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "agregar":
            nombre = request.form.get("nombre", "").strip()
            direccion = request.form.get("direccion", "").strip()
            telefono = request.form.get("telefono", "").strip()
            fecha = request.form.get("fecha", obtener_fecha_hoy().isoformat()).strip()

            tamano = request.form.get("tamano", "").strip()
            numero_pizzas = request.form.get("numero_pizzas", "").strip()
            ingredientes = request.form.getlist("ingredientes")

            fecha_convertida = convertir_fecha_desde_formulario(fecha)

            if not nombre or not direccion or not telefono:
                flash("Complete los datos del cliente.", "warning")
            elif not fecha_convertida:
                flash("Seleccione una fecha válida.", "warning")
            elif tamano not in PRECIOS:
                flash("Seleccione un tamaño válido.", "warning")
            elif not numero_pizzas.isdigit() or int(numero_pizzas) < 1:
                flash("Ingrese una cantidad válida de pizzas.", "warning")
            else:
                numero_pizzas = int(numero_pizzas)
                precio_unitario = calcular_precio_unitario(tamano, ingredientes)
                subtotal = precio_unitario * numero_pizzas

                item = {
                    "tamano": tamano,
                    "ingredientes": ", ".join(ingredientes) if ingredientes else "Sin ingredientes extra",
                    "ingredientes_lista": ingredientes,
                    "numero_pizzas": numero_pizzas,
                    "precio_unitario": float(precio_unitario),
                    "subtotal": float(subtotal)
                }

                detalle.append(item)
                session["detalle_pedido"] = detalle
                session["datos_cliente"] = {
                    "nombre": nombre,
                    "direccion": direccion,
                    "telefono": telefono,
                    "fecha": fecha
                }
                session.modified = True

                flash("Pizza agregada correctamente al detalle.", "success")
                return redirect(url_for("pizzeria.index"))

        elif accion == "quitar":
            index_item = request.form.get("index", "").strip()

            if index_item.isdigit():
                index_item = int(index_item)
                if 0 <= index_item < len(detalle):
                    detalle.pop(index_item)
                    session["detalle_pedido"] = detalle
                    session.modified = True
                    flash("Pizza eliminada del detalle.", "danger")

            return redirect(url_for("pizzeria.index"))

        elif accion == "terminar":
            nombre = request.form.get("nombre", datos_cliente.get("nombre", "")).strip()
            direccion = request.form.get("direccion", datos_cliente.get("direccion", "")).strip()
            telefono = request.form.get("telefono", datos_cliente.get("telefono", "")).strip()
            fecha = request.form.get("fecha", datos_cliente.get("fecha", obtener_fecha_hoy().isoformat())).strip()

            fecha_pedido = convertir_fecha_desde_formulario(fecha)

            if not nombre or not direccion or not telefono:
                flash("Complete los datos del cliente.", "warning")
            elif not fecha_pedido:
                flash("Seleccione una fecha válida.", "warning")
            elif len(detalle) == 0:
                flash("Agrega al menos una pizza antes de terminar el pedido.", "warning")
            else:
                cliente = obtener_o_crear_cliente(nombre, direccion, telefono)
                total = calcular_total(detalle)

                pedido = Pedido(
                    id_cliente=cliente.id_cliente,
                    fecha=fecha_pedido,
                    total=total
                )
                db.session.add(pedido)
                db.session.flush()

                for item in detalle:
                    pizza = obtener_o_crear_pizza(
                        tamano=item["tamano"],
                        ingredientes=item["ingredientes"],
                        precio=item["precio_unitario"]
                    )

                    det = DetallePedido(
                        id_pedido=pedido.id_pedido,
                        id_pizza=pizza.id_pizza,
                        cantidad=item["numero_pizzas"],
                        subtotal=item["subtotal"]
                    )
                    db.session.add(det)

                db.session.commit()

                limpiar_sesion_pedido()

                flash(
                    f"Pedido registrado correctamente. Total a pagar: ${total:.2f}",
                    "success"
                )
                return redirect(url_for("pizzeria.index"))

    ventas_hoy, total_hoy = obtener_ventas_hoy()

    return render_template(
        "pizzeria/index.html",
        form=form,
        detalle=detalle,
        total=calcular_total(detalle),
        datos_cliente=datos_cliente,
        ventas_hoy=ventas_hoy,
        total_hoy=total_hoy
    )


@pizzeria.route("/pizzeria/ventas-dia", methods=["GET", "POST"])
def ventas_dia():
    form = ConsultaDiaForm()
    resultados = []
    total = 0
    resumen = None
    hoy = obtener_fecha_hoy()

    filtros = {
        "dia_semana": str(hoy.weekday()),
        "mes": str(hoy.month),
        "anio": str(hoy.year)
    }

    if request.method == "POST":
        filtros["dia_semana"] = request.form.get("dia_semana", str(hoy.weekday())).strip()
        filtros["mes"] = request.form.get("mes", str(hoy.month)).strip()
        filtros["anio"] = request.form.get("anio", str(hoy.year)).strip()

        if not filtros["dia_semana"] or not filtros["mes"] or not filtros["anio"]:
            flash("Seleccione día de semana, mes y año.", "warning")
        else:
            dia_semana = int(filtros["dia_semana"])
            mes = int(filtros["mes"])
            anio = int(filtros["anio"])

            pedidos_mes = (
                Pedido.query
                .filter(
                    extract("year", Pedido.fecha) == anio,
                    extract("month", Pedido.fecha) == mes
                )
                .order_by(Pedido.fecha.asc(), Pedido.id_pedido.asc())
                .all()
            )

            resultados = [p for p in pedidos_mes if p.fecha.weekday() == dia_semana]
            total = sum(float(p.total) for p in resultados)
            resumen = f"{DIAS_SEMANA[dia_semana]}s de {MESES[mes]} {anio}"

            if not resultados:
                flash("No hay ventas para esa consulta.", "warning")
    else:
        dia_semana = hoy.weekday()
        mes = hoy.month
        anio = hoy.year

        pedidos_mes = (
            Pedido.query
            .filter(
                extract("year", Pedido.fecha) == anio,
                extract("month", Pedido.fecha) == mes
            )
            .order_by(Pedido.fecha.asc(), Pedido.id_pedido.asc())
            .all()
        )

        resultados = [p for p in pedidos_mes if p.fecha.weekday() == dia_semana]
        total = sum(float(p.total) for p in resultados)
        resumen = f"{DIAS_SEMANA[dia_semana]}s de {MESES[mes]} {anio}"

    return render_template(
        "pizzeria/ventas_dia.html",
        form=form,
        resultados=resultados,
        total=total,
        resumen=resumen,
        filtros=filtros
    )


@pizzeria.route("/pizzeria/ventas-mes", methods=["GET", "POST"])
def ventas_mes():
    form = ConsultaMesForm()
    resultados = []
    total = 0
    resumen = None
    hoy = obtener_fecha_hoy()

    filtros = {
        "mes": str(hoy.month),
        "anio": str(hoy.year)
    }

    if request.method == "POST":
        filtros["mes"] = request.form.get("mes", str(hoy.month)).strip()
        filtros["anio"] = request.form.get("anio", str(hoy.year)).strip()

        if not filtros["mes"] or not filtros["anio"]:
            flash("Seleccione mes y año.", "warning")
        else:
            mes = int(filtros["mes"])
            anio = int(filtros["anio"])

            resultados = (
                Pedido.query
                .filter(
                    extract("year", Pedido.fecha) == anio,
                    extract("month", Pedido.fecha) == mes
                )
                .order_by(Pedido.fecha.asc(), Pedido.id_pedido.asc())
                .all()
            )

            total = sum(float(p.total) for p in resultados)
            resumen = f"{MESES[mes]} {anio}"

            if not resultados:
                flash("No hay ventas para ese mes.", "warning")
    else:
        mes = hoy.month
        anio = hoy.year

        resultados = (
            Pedido.query
            .filter(
                extract("year", Pedido.fecha) == anio,
                extract("month", Pedido.fecha) == mes
            )
            .order_by(Pedido.fecha.asc(), Pedido.id_pedido.asc())
            .all()
        )

        total = sum(float(p.total) for p in resultados)
        resumen = f"{MESES[mes]} {anio}"

    return render_template(
        "pizzeria/ventas_mes.html",
        form=form,
        resultados=resultados,
        total=total,
        resumen=resumen,
        filtros=filtros
    )


@pizzeria.route("/pizzeria/detalle-venta", methods=["GET"])
def detalle_venta():
    pedido_id = request.args.get("id", "").strip()
    volver = request.args.get("volver", "pizzeria.index")

    if not pedido_id.isdigit():
        flash("Identificador de venta inválido.", "warning")
        return redirect(url_for("pizzeria.index"))

    pedido = Pedido.query.filter_by(id_pedido=int(pedido_id)).first()

    if not pedido:
        flash("Venta no encontrada.", "warning")
        return redirect(url_for("pizzeria.index"))

    return render_template(
        "pizzeria/detalle_venta.html",
        pedido=pedido,
        volver=volver
    )