import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


# Use a service account.
cred = credentials.Certificate("lps.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()
cadets=db.collection("Cadets")

presentGen = (
    cadets
    .where(filter=FieldFilter("at", "==", "present"))
    .stream()
)
def number(docsGen):
   docs=[]
   for doc in docsGen:
      docs.append(doc.id)
   return docs
   
state=[number(presentGen)]
print(state)