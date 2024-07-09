from app import db, TravelPackage, app

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        package1 = TravelPackage(origin="Mumbai", destination="London", price=1000, details="5-star hotel, guided tours")
        package2 = TravelPackage(origin="Hong Kong", destination="London", price=1200, details="4-star hotel, sightseeing")
        
        db.session.add(package1)
        db.session.add(package2)
        db.session.commit()

if __name__ == '__main__':
    init_db()
