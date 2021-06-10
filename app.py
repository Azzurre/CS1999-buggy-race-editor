from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import json
import unittest

# app - The flask application where all the magical things are configured.
app = Flask(__name__)


# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone(); 
        return render_template("buggy-form.html", buggy=None)

    elif request.method == 'POST':
        
        msg=""
        violations=""
        violations1=""
        violations2=""
        violations3=""
        violations4=""


        buggy_id = request.form['id']
        qty_wheels = request.form['qty_wheels']
        power_type = request.form['power_type']
        aux_power_type = request.form['aux_power_type']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        algo = request.form['algo']
        antibiotic = request.form['antibiotic']
        insulated = request.form['insulated']
        banging = request.form['banging']
        power_units = request.form['power_units']
        aux_power_units = request.form['aux_power_units']
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        hamster_booster = request.form['hamster_booster']



        if int(qty_wheels) < 4:
            violations = f"RULE VIOLATION ({qty_wheels} wheels)"
        if not qty_wheels.isdigit():
            msg = f"{qty_wheels} is not a number"     
            return render_template("buggy-form.html", msg = msg, buggy=None)
        elif flag_color == flag_color_secondary:
            violations1 = f"RULE VIOLATION (You cannot use the same colours, you might as well pick plain)"
            return render_template("buggy-form.html", violations1 = violations1, buggy=None)
        elif power_type == aux_power_type:
            violations2 = f"RULE VIOLATION (You cannot have the same type of backup power as the primary)"
            return render_template("buggy-form.html", violations2 = violations2, buggy=None)
        elif qty_wheels != qty_tyres:
            violations3 = f"RULE VIOLATION (The amount of tyres and the amount of wheels have to be equal)"
            return render_template("buggy-form.html", violations3 = violations3, buggy=None)

#       COST STUFF AND BALANCE
        balance = 0
        cost_petrol = 4
        cost_fusion = 400
        cost_steam = 3
        cost_bio = 5
        cost_electric = 20
        cost_rocket = 16
        cost_hamster = 3
        cost_thermo = 300
        cost_solar = 40
        cost_wind = 20
        
        cost_knobbly = 15
        cost_slick = 10
        cost_steelband = 20
        cost_reactive = 40
        cost_maglev = 50

        cost_noarmour = 0
        cost_wood = 40
        cost_aluminium = 200
        cost_thinsteel = 100
        cost_thicksteel = 200
        cost_titanium = 290

        cost_noattack = 0
        cost_spike = 5
        cost_flame = 20
        cost_charge = 28
        cost_biohazard = 30

        cost_fireproof = 70
        cost_banging = 42
        cost_antibiotic = 90
        cost_insulated = 100
#       FUELS
        if power_type == "petrol":
            balance = balance + int(power_units)*cost_petrol
        elif power_type == "fusion":
            balance = balance + int(power_units)*cost_fusion
        elif power_type == "steam":
            balance = balance + int(power_units)*cost_steam
        elif power_type == "bio":
            balance = balance + int(power_units)*cost_bio
        elif power_type == "electric":
            balance = balance + int(power_units)*cost_electric
        elif power_type == "rocket":
            balance = balance + int(power_units)*cost_rocket
        elif power_type == "hamster":
            balance = balance + int(power_units)*cost_hamster
        elif power_type == "thermo":
            balance = balance + int(power_units)*cost_thermo
        elif power_type == "solar":
            balance = balance + int(power_units)*cost_solar
        elif power_type == "wind":
            balance = balance + int(power_units)*cost_wind
        print(balance)
#       FUELS AUX
        if aux_power_type == "petrol":
            balance = balance + int(aux_power_units)*cost_petrol
        elif aux_power_type == "fusion":
            balance = balance + int(aux_power_units)*cost_fusion
        elif aux_power_type == "steam":
            balance = balance + int(aux_power_units)*cost_steam
        elif aux_power_type == "bio":
            balance = balance + int(aux_power_units)*cost_bio
        elif aux_power_type == "electric":
            balance = balance + int(aux_power_units)*cost_electric
        elif aux_power_type == "rocket":
            balance = balance + int(aux_power_units)*cost_rocket
        elif aux_power_type == "hamster":
            balance = balance + int(aux_power_units)*cost_hamster
        elif aux_power_type == "thermo":
            balance = balance + int(aux_power_units)*cost_thermo
        elif aux_power_type == "solar":
            balance = balance + int(aux_power_units)*cost_solar
        elif aux_power_type == "wind":
            balance = balance + int(aux_power_units)*cost_wind
        print(balance)
#       TYRES
        if tyres == "knobbly":
            balance = balance + cost_knobbly*int(qty_tyres)
        elif tyres == "slick":
            balance = balance + cost_slick*int(qty_tyres)
        elif tyres == "steelband":
            balance = balance + cost_steelband*int(qty_tyres)
        elif tyres == "reactive":
            balance = balance + cost_reactive*int(qty_tyres)
        elif tyres == "maglev":
            balance = balance + cost_maglev*int(qty_tyres)
        print(balance)
#       ARMOUR
        if armour == "none":
            balance = balance + int(cost_noarmour)
        elif armour == "wood":
            balance = balance + int(cost_wood)
        elif armour == "aluminium":
            balance = balance + int(cost_aluminium)
        elif armour == "thinsteel":
            balance = balance + int(cost_thinsteel)
        elif armour == "thicksteel":
            balance = balance + int(cost_thicksteel)
        elif armour == "titanium":
            balance = balance + int(cost_titanium)
        print(balance)
#       ATTACKS
        if attack == "none":
            balance = balance + cost_noattack*int(qty_attacks)
        elif attack == "spike":
            balance = balance + cost_spike*int(qty_attacks)
        elif attack == "flame":
            balance = balance + cost_flame*int(qty_attacks)
        elif attack == "charge":
            balance = balance + cost_charge*int(qty_attacks)
        elif attack == "biohazard":
            balance = balance + cost_biohazard*int(qty_attacks)
        print(balance)
#       FIREPROOF
        if fireproof == "yes":
            balance = balance + cost_fireproof
        elif fireproof == "no":
            balance = balance
        print(balance)
#       INSULATION
        if insulated == "yes":
            balance = balance + cost_insulated
        elif insulated == "no":
            balance = balance
        print(balance)
#       ANTIBIOTIC
        if antibiotic == "yes":
            balance = balance + cost_antibiotic
        elif antibiotic == "no":
            balance = balance
        print(balance)
#       SOUND SYSTEM
        if banging == "yes":
            balance = balance + cost_banging
        elif banging == "no":
            balance = balance
        print(balance)

        if balance > 200:
            msg = f"RULE VIOLATION (Your buggy has to cost less than or equal to 200)"     
            return render_template("buggy-form.html", msg = msg, buggy=None)

    
        #TEST
        
        if balance == 64:
            print("The cost is accurate.")
        else:
            print(balance, "The cost is not accurate.")
        #TEST
   
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                if buggy_id:
                    cur.execute(
                        "UPDATE buggies set qty_wheels=?, power_type=?, hamster_booster=?, power_units=?, aux_power_units=?, banging=?, aux_power_type=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, algo=?, antibiotic=?, insulated=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, balance=? WHERE id=?",
                        (qty_wheels, power_type, hamster_booster, power_units, aux_power_units, banging, aux_power_type, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, algo, antibiotic, insulated, flag_color, flag_color_secondary, flag_pattern, balance, buggy_id)
                    )
                else:
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, power_type, hamster_booster, power_units, aux_power_units, banging, aux_power_type, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, algo, antibiotic, insulated, flag_color, flag_color_secondary, flag_pattern, balance) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (qty_wheels, power_type, hamster_booster, power_units, aux_power_units, banging, aux_power_type, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, algo, antibiotic, insulated, flag_color, flag_color_secondary, flag_pattern, balance,)
                    )
                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg, violations = violations, violations1 = violations1, violations2 = violations2, violations3 = violations3, violations4 = violations4)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall(); 
    return render_template("buggy.html", buggies = records)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    print (f"I want to edit buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone(); 
    return render_template("buggy-form.html", buggy=record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 3-DEL
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
    print (f"I want to edit buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("delete FROM buggies WHERE id=?", (buggy_id,))
    con.commit()
    return render_template("buggy.html")


#------------------------------------------------------------
#POSTER
##------------------------------------------------------------

@app.route('/poster')
def poster():
   return render_template('poster.html')


#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")

