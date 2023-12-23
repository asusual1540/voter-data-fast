import uuid
from typing import Iterator

from fastapi import HTTPException
from fastapi.responses import JSONResponse

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

    def get_by_id(self, voter_id: int) -> Voter:
        with self.db() as session:
            voter = session.query(Voter).filter(Voter.voter_no == voter_id).first()
            return voter
        
    def get_voter(self, per_page, page, name, voter_no, father_name, mother_name, occupation, address, area_id):
        with self.db() as session:
            if per_page is None:
                per_page = 10
            if page is None:
                page = 1
            query = session.query(Voter)
            
            print('query',query)
            
            print("all-data-->", per_page, page, name, voter_no, father_name, mother_name, occupation, address, area_id)
            if name:
                query = query.filter(Voter.name.contains(name))
            if voter_no:
                query = query.filter(Voter.voter_no.contains(voter_no))
            if father_name:
                query = query.filter(Voter.father_name.contains(father_name))
            if mother_name:
                query = query.filter(Voter.mother_name.contains(mother_name))
            if occupation:
                query = query.filter(Voter.occupation.contains(occupation))
            if address:
                query = query.filter(Voter.address.contains(address))
            if area_id:
                query = query.filter(Voter.area_id.contains(area_id))
            

            total_records = query.count()

            if page and per_page:
                query = query.offset((page - 1) * per_page).limit(per_page)

            voters = query.all()

            voter_list = [voter.as_dict() for voter in voters]
            for voter in voter_list:
                print("voter", voter)
                if voter["area_id"] is not None:
                    query_area = session.query(Area).filter(Area.id == voter["area_id"]).first()
                    voter["area"] = query_area.as_dict()

            response_data = {"voters": voter_list, "total_records": total_records}
            
            print('response=======================',response_data)
            # content = json.dumps(response_data, default=str)

            return JSONResponse(content=response_data)
        
    def get_voter_area(self, per_page, page, gender, district, sub_district, city_corporation, union, ward_no, voter_area, total_voter, voter_area_no, total_voter_female):
        with self.db() as session:
            query = session.query(Area)
            
            print('query', query)
            
            print("all-data-->", per_page, page, gender, district, sub_district, city_corporation, union, ward_no, voter_area, total_voter, voter_area_no, total_voter_female)
            if gender:
                query = query.filter(Voter.gender == gender)
            if district:
                query = query.filter(Voter.district.contains(district))
            if sub_district:
                query = query.filter(Voter.sub_district.contains(sub_district))
            if city_corporation:
                query = query.filter(Voter.city_corporation.contains(city_corporation))
            if union:
                query = query.filter(Voter.union.contains(union))
            if ward_no:
                query = query.filter(Voter.ward_no == ward_no)
            if voter_area:
                query = query.filter(Voter.voter_area.contains(voter_area))
            if total_voter:
                query = query.filter(Voter.total_voter == total_voter)
            if voter_area_no:
                query = query.filter(Voter.voter_area_no.contains(voter_area_no))
            if total_voter_female:
                query = query.filter(Voter.total_voter_female == total_voter_female)
            

            total_records = query.count()

            if page and per_page:
                query = query.offset((page - 1) * per_page).limit(per_page)

            voter_areas = query.all()

            area_list = [voter_area.as_dict() for voter_area in voter_areas]
            response_data = {"areas": area_list, "total_records": total_records}
            
            print('response=======================',response_data)
            # content = json.dumps(response_data, default=str)

            return JSONResponse(content=response_data)
        
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
