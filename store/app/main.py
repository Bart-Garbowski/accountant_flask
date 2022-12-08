from flask import Flask, render_template, request, flash


#saldo = 1200

store_data = {
    "rower": {"price": 100.0, "counts": 2},
    "chleb": {"price": 6.0, "counts": 12}
}

app = Flask(__name__)
app.config["SECRET_KEY"]="12345"
app.saldo = 1200
app.historia = []

def return_template(error_message=None):
    context = {
        "home": store_data,
        "saldo": app.saldo
    }
    if error_message:
        flash(error_message)
    return render_template("home.html", context=context)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        operation = request.form.get("operation")
        if operation == "kupno":
            product_name = request.form["product_name"]
            product_count = request.form["product_count"]
            product_price = request.form["product_price"]
            if product_name == "" or product_count == "" or product_price == "":
                return return_template("Uzupelnij poprawnie dane")
            
            else:
                product_count = int(request.form["product_count"])
                product_price = int(request.form["product_price"])
                store_data[product_name] = {"price": product_price, "counts": product_count}
                total_price = product_count * product_price
                app.saldo -= total_price
                msg = f" Kupno: {product_name}. Sztuk: {product_count}. Cena: {product_price}"
                app.historia.append(msg)

        elif operation == "sprzedaz":
            product_name = request.form["product_name"]
            product_count = request.form["product_count"]
            if product_name == "" or not product_count.isdigit():
                return return_template("Uzupelnij poprawnie dane")
            product_count = int(product_count)
            
            if product_name in store_data:
                price = int(store_data[product_name]["price"])
                if product_count > store_data[product_name]["counts"]:
                    return return_template("Uzupelnij poprawnie dane")

                store_data[product_name]["counts"] -= product_count
                total_price = product_count * price
                print(app.saldo)
                app.saldo += total_price
                msg = f" Sprzedaz: {product_name}. Sztuk: {product_count}."
                app.historia.append(msg)

        elif operation == "zmiana_salda":
            komentarz = request.form["komentarz"]
            wartosc = request.form["wartosc"]
            if komentarz == "":
                return return_template("Uzupelnij poprawnie dane")
            try:
                wartosc = float(wartosc)
            except ValueError:
                return return_template("Uzupelnij poprawnie dane")
            app.saldo += wartosc
            msg = f" Zmiana salda: {wartosc}. Komentarz: {komentarz}."
            app.historia.append(msg)
                
    return return_template()


@app.route("/history")
def history():
    context={
        "historia": app.historia
    }
    return render_template("history.html", context=context)
