import uuid
from typing import Iterator

from fastapi import HTTPException

from app.api.voter.voter_model import Area, Voter

def generate_unique_id():
    unique_id = str(uuid.uuid4())
    return unique_id

class VoterService:
    def __init__(self, config, db, authentication_service):
        self.config = config
        self.db = db
        self.authentication_service = authentication_service

    
    def get_all(self) -> Iterator[Voter]:
        with self.db() as session:
            return session.query(Voter).all()

    def get_by_id(self, credit_id: int) -> Voter:
        with self.db() as session:
            credit = session.query(Voter).filter(Voter.id == credit_id).first()
            return credit
        
        
    def add_voter(self, voter_create) -> Voter:
        print("voter_create", voter_create)
        with self.db() as session:
            # Check if the specified area_id exists
            existing_area = session.query(Area).filter(Area.id == voter_create.area_id).first()

            if existing_area is None:
                # raise HTTPException(status_code=404, detail="Area not found")
                print("Area not found")
            new_voter = {
                'id': str(uuid.uuid4()),
                'name': voter_create.name,
                'voter_no': voter_create.voter_no,
                'father_name': voter_create.father_name,
                'mother_name': voter_create.mother_name,
                'occupation': voter_create.occupation,
                'address': voter_create.address,
            }
            # Create the voter with the specified area_id
            voter = Voter(**new_voter)
            voter.area = existing_area  # Assign the area relationship
            session.add(voter)
            session.commit()
            session.refresh(voter)
            return voter
        
    def add_area(self, area_create) -> Area:
        print("area_create", area_create)
        with self.db() as session:
            # Check if the specified area_id exists
            # existing_area = session.query(Area).filter(Area.id == area_create.area_id).first()
            new_area = {
                'id': str(uuid.uuid4()),
                'gender': area_create.gender,
                'district': area_create.district,
                'sub_district': area_create.sub_district,
                'city_corporation': area_create.city_corporation,
                'union': area_create.union,
                'ward_no': area_create.ward_no,
                'voter_area': area_create.voter_area,
                'total_voter': area_create.total_voter,
                'voter_area_no': area_create.voter_area_no,
                'total_voter_female': area_create.total_voter_female
            }
            area = Area(**new_area)
            session.add(area)
            session.commit()
            session.refresh(area)
            return area
