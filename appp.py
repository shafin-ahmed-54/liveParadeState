from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.Certificate("lps1.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

cadets=db.collection("Cadets")

admin=0

def cdetdetail(docsGen):
   docs=[]
   cdtno=[]
   for doc in docsGen:
      docs.append(doc.to_dict())
      cdtno.append(doc.id)
   return cdtno,docs

def number(docsGen):
   number=[]
   for doc in docsGen:
      number.append(doc.id)
   return len(number)

def getAll():
   cdtdetails=cadets.stream()
   cdtno,docs=cdetdetail(cdtdetails)
   return [cdtno,docs]


def getNumberGen(field=[],value=[],data=0):
   if len(field)==0:
      presentGen = (
      cadets
      .where(filter=FieldFilter("at", "==", "present"))
      .stream()
      )
      hospitalGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "hospital"))
         .stream()
      )
      cmhGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "cmh"))
         .stream()
      )
      leaveGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "leave"))
         .stream()
      )
   elif len(field)==1:
      presentGen = (
      cadets
      .where(filter=FieldFilter("at", "==", "present")).where(filter=FieldFilter(field[0], "==", value[0]))
      .stream()
      )
      hospitalGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "hospital")).where(filter=FieldFilter(field[0], "==", value[0]))
         .stream()
      )
      cmhGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "cmh")).where(filter=FieldFilter(field[0], "==", value[0]))
         .stream()
      )
      leaveGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "leave")).where(filter=FieldFilter(field[0], "==", value[0]))
         .stream()
      )
   else:
      presentGen = (
      cadets
      .where(filter=FieldFilter("at", "==", "present")).where(filter=FieldFilter(field[0], "==", value[0])).where(filter=FieldFilter(field[1], "==", value[1]))
      .stream()
      )
      hospitalGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "hospital")).where(filter=FieldFilter(field[0], "==", value[0])).where(filter=FieldFilter(field[1], "==", value[1]))
         .stream()
      )
      cmhGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "cmh")).where(filter=FieldFilter(field[0], "==", value[0])).where(filter=FieldFilter(field[1], "==", value[1]))
         .stream()
      )
      leaveGen = (
         cadets
         .where(filter=FieldFilter("at", "==", "leave")).where(filter=FieldFilter(field[0], "==", value[0])).where(filter=FieldFilter(field[1], "==", value[1]))
         .stream()
      )
   if data==0:
      state=[number(presentGen),number(hospitalGen),number(cmhGen),number(leaveGen)]
      return state
   else:
      cdtdetail= [cdetdetail(presentGen),cdetdetail(hospitalGen),cdetdetail(cmhGen),cdetdetail(leaveGen)]
      return (cdtdetail)

def getCadetbyname(value):
   cadet=cadets.where(filter=FieldFilter("name", "==", value)).stream()
   for doc in cadet:
      return doc.id,doc.to_dict()
   
def getCadetbycdtno(value):
   cadet=cadets.document(f'{value}').get()
   print(value)
   return cadet.id,cadet.to_dict()

app = Flask(__name__)
  
@app.route("/")
def index():
   state=getNumberGen(data=0)
   cdtdetail=getAll()
   print(state)
   return render_template("index.html",  admin=admin,total=len(cdtdetail[0]),present=state[0],hospital=state[1],cmh=state[2],leave=state[3])

@app.route("/kh")
def kh():
   state=getNumberGen(['house'],['Khalid'],data=0)
   total=state[0]+state[1]+state[2]+state[3]
   return render_template("kh.html",  admin=admin, total=total, present=state[0],hospital=state[1],cmh=state[2],leave=state[3])

@app.route("/qh")
def qh():
   state=getNumberGen(['house'],['Qasim'],data=0)
   total=state[0]+state[1]+state[2]+state[3]
   return render_template("qh.html", admin=admin, total=total, present=state[0],hospital=state[1],cmh=state[2],leave=state[3])

@app.route("/th")
def th():
   state=getNumberGen(['house'],['Tariq'],data=0)
   total=state[0]+state[1]+state[2]+state[3]
   return render_template("th.html",  admin=admin, total=total, present=state[0],hospital=state[1],cmh=state[2],leave=state[3])

@app.route("/form/<at>")
def form(at):
   if at=="viiA":
      state=getNumberGen(['class','form',],['VII', 'A'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="VII A", fm='MD Amirul Islam', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="viiB":
      state=getNumberGen(['class','form',],['VII', 'B'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin,at=at, total=total,formName="VII B", fm='Rajat Goshwami', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="viiiA":
      state=getNumberGen(['class','form',],['VIII', 'A'])
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="VIII A", fm='Ms Hasina Banu', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="viiiB":
      state=getNumberGen(['class','form',],['VIII', 'B'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="VIII B", fm='MD Makfur rahman', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="ixA":
      state=getNumberGen(['class''form',],['IX', 'B'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,formName="IX B", fm='MD Mosharrof Hossain', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="ixB":
      state=getNumberGen(['class','form',],['IX', 'A'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="IX A", fm='Ms Kamrunnahar Akand', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xA":
      state=getNumberGen(['class','form',],['X', 'A'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="X A", fm='MD Taijul Islam', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xB":
      state=getNumberGen(['class','form',],['X', 'B'])
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="X B", fm='MD Amirul Islam', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xiA":
      state=getNumberGen(['class','form',],['XI', 'A'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="XI A", fm='MD Amimul Ahsan Mahfuz', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xiB":
      state=getNumberGen(['class','form',],['XI', 'B'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at, total=total,formName="XI B", fm='MD Mosaddequr Rahman', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xiiA":
      state=getNumberGen(['class','form',],['XII', 'A'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at,total=total,formName="XII A", fm='MD Samsul Arefin Shaon', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   if at=="xiiB":
      state=getNumberGen(['class','form',],['XII', 'B'])
      total=state[0]+state[1]+state[2]+state[3]
      return render_template("form.html", loc=at, admin=admin, at=at, total=total,formName="XII B", fm='Ms Dilara Afroz', present=state[0],hospital=state[1],cmh=state[2],leave=state[3])
   

@app.route("/total/<loc>")
def total(loc):
   print(loc)

   if loc=='all':
      cdtdetail=getAll()
      print(cdtdetail)
      return render_template("total.html", loc=loc, admin=admin,title="Total Cadets", data=cdtdetail, len=len(cdtdetail[0]))

   elif loc=='tariq' or loc=='qasim' or loc=='khalid':
      loc=loc.capitalize()
      cdtdetail=getNumberGen(['house'],[loc],data=1)
      print(cdtdetail)
      return render_template("totall.html", loc=loc, admin=admin,title=f"Total Cadets in {loc} House", data=cdtdetail, len=len(cdtdetail[0][0]))
   else:
      print(loc)
      cdtdetail=getNumberGen(['class','form'],[loc[:len(loc)-1].upper(),loc[-1]],data=1)
      print(cdtdetail)
      return render_template("totall.html", loc=loc, admin=admin,title=f"Total Cadets in Form {loc}", data=cdtdetail, len=len(cdtdetail[0][0]))
   
@app.route("/present/<loc>")
def present(loc):
   print(loc)
   if loc=='all':
      cdtdetail=getNumberGen(data=1)
      print(cdtdetail)
      return render_template("present.html", loc=loc, admin=admin, title="Total Present",data=cdtdetail, len=len(cdtdetail[0][0]))
   
   elif loc=='tariq' or loc=='qasim' or loc=='khalid':
      loc=loc.capitalize()
      cdtdetail=getNumberGen(['house','at'],[loc,'present'],data=1)
      print(cdtdetail)
      return render_template("present.html", loc=loc, admin=admin,title=f"Total Cadets Present in {loc} House", data=cdtdetail, len=len(cdtdetail[0][0]))
   else:
      print(loc)
      cdtdetail=getNumberGen(['class','form','at'],[loc[:len(loc)-1].upper(),loc[-1],'present'],data=1)
      print(cdtdetail)
      return render_template("present.html", loc=loc, admin=admin,title=f"Total Cadets in Form {loc[:2].upper()} {loc[-1]}", data=cdtdetail, len=len(cdtdetail[0][0]))
   
@app.route("/cmh/<loc>")
def cmh(loc):
   print(loc)
   if loc=='all':
      cdtdetail=getNumberGen(["at"],["cmh"],data=1)
      print(cdtdetail)
      return render_template("cmh.html", loc=loc, admin=admin, title="Total Cadets at CMH", data=cdtdetail, len=len(cdtdetail[2][0]))
   
   elif loc=='tariq' or loc=='qasim' or loc=='khalid':
      loc=loc.capitalize()
      cdtdetail=getNumberGen(['house','at'],[loc,'cmh'],data=1)
      print(cdtdetail)
      return render_template("cmh.html", loc=loc, admin=admin,title=f"Total Cadets at CMH of {loc} House", data=cdtdetail, len=len(cdtdetail[2][0]))
   else:
      print(loc)
      cdtdetail=getNumberGen(['class','form','at'],[loc[:len(loc)-1].upper(),loc[-1],'present'],data=1)
      print(cdtdetail)
      return render_template("cmh.html", loc=loc, admin=admin,title=f"Total Cadets at CMH of Form {loc[:2].upper()} {loc[-1]}", data=cdtdetail, len=len(cdtdetail[2][0]))
   
@app.route("/hospital/<loc>")
def hospital(loc):
   print(loc)
   if loc=='all':
      cdtdetail=getNumberGen(["at"],["hospital"], data=1)
      print(cdtdetail)
      return render_template("hospital.html", loc=loc, admin=admin, title="Total Cadets at Hospital", data=cdtdetail, len=len(cdtdetail[1][0]))
   
   elif loc=='tariq' or loc=='qasim' or loc=='khalid':
      loc=loc.capitalize()
      cdtdetail=getNumberGen(['house','at'],[loc,'hospital'],data=1)
      print(cdtdetail)
      return render_template("hospital.html", loc=loc, admin=admin,title=f"Total Cadets at Hospital of {loc} House", data=cdtdetail, len=len(cdtdetail[1][0]))
   else:
      print(loc)
      cdtdetail=getNumberGen(['class','form','at'],[loc[:len(loc)-1].upper(),loc[-1],'hospital'],data=1)
      print(cdtdetail)
      return render_template("hospital.html", loc=loc, admin=admin,title=f"Total Cadets at Hospital of Form {loc[:2].upper()} {loc[-1]}", data=cdtdetail, len=len(cdtdetail[1][0]))
   

@app.route("/leave/<loc>")
def leave(loc):
   print(loc)
   if loc=='all':
      cdtdetail=getNumberGen(["at"],["leave"],data=1)
      print(cdtdetail)
      return render_template("leave.html", loc=loc, admin=admin, title="Total Cadets at Leave",  data=cdtdetail, len=len(cdtdetail[3][0]))
   
   elif loc=='tariq' or loc=='qasim' or loc=='khalid':
      loc=loc.capitalize()
      cdtdetail=getNumberGen(['house','at'],[loc,'leave'],data=1)
      print(cdtdetail)
      return render_template("leave.html", loc=loc, admin=admin,title=f"Total Cadets at Leave of {loc} House", data=cdtdetail, len=len(cdtdetail[3][0]))
   else:
         print(loc)
         cdtdetail=getNumberGen(['class','form','at'],[loc[:len(loc)-1].upper(),loc[-1],'leave'],data=1)
         print(cdtdetail)
         return render_template("leave.html", loc=loc, admin=admin,title=f"Total Cadets at Leave of Form {loc[:2].upper()} {loc[-1]}", data=cdtdetail, len=len(cdtdetail[3][0]))
   

@app.route('/cadet', methods =["GET", "POST"])
def cadet():
   input=request.form.get("input")
   print(input)
   try: 
      int(input)
      cdtno,cdtdetail=getCadetbycdtno(input)
   except:
      input=input.capitalize()
      cdtno,cdtdetail=getCadetbyname(input)
   
   print(cdtdetail)
   return render_template("cadet.html", admin=admin, cdtdetail=cdtdetail,cdtno=cdtno)

@app.route('/change', methods =["GET", "POST"])
def change():
   cdtn = request.args.get("cdtno")
   location = request.args.get("changed")
   cadets.document(str(cdtn)).update({"at": location.lower()})
   cdtno,cdtdetail=getCadetbycdtno(cdtn)
   print(cdtdetail)
   return render_template("cadet.html", loc=loc, admin=admin, cdtdetail=cdtdetail,cdtno=cdtno)

@app.route('/login', methods =["GET", "POST"])
def login():
   user=request.form.get("uname")
   psw=request.form.get("psw")
   pos=request.form.get("pos")
   frm=request.form.get("from")
   if user=='admin':
        if psw=='admin':
             global admin
             admin=1
   return pos(frm)

@app.route('/logout', methods =["GET", "POST"])
def logout():
   global admin
   admin=0
   return index()

if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True)