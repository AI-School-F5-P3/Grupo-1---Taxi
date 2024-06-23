from class_firebase_database import FirebaseDB

path = "taximetro-5503c-firebase-adminsdk-vbmrg-dfd43417a3.json"
url = "https://taximetro-5503c-default-rtdb.europe-west1.firebasedatabase.app/"

fb_db = FirebaseDB(path, url)

data = {
    'trip_id': '4',
    'driver_name': 'Pedro',
    'passenger_name': 'Erika',
    'license_plate': 'ABC123',
    'passenger_count': 2,
    'event': 'end' ,
    'time': '2024-06-22 22:17:15',
    'total_time':71.49006962776184,
    'total_pause_time': 71.49006962776184,
    'fare': 63.00252676010132,
    'initial_distance': 1.4243771433830261,
    'final_distance': 13.199999999999763,
    'total_distance': 13.199999999999763    
}

fb_db.write_record('/taximetro1/4', data)