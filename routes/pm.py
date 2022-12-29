from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException

from config.db import pmDb
from models.pm import PmStatus
from schemas.utils import serializeDict, serializeList

pm = APIRouter(prefix='/pm')

@pm.get('/{pole_id}')
async def find_pm_status(pole_id,day: int = 1):
    try:
        lastweek = datetime.timestamp(datetime.now() -timedelta(days=day))
        return serializeList(pmDb.find({"poleId":pole_id, "timestamp": {"$gt": lastweek}}))
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@pm.post('/{pole_id}')
async def create_pm_status(pole_id, pmStatus : PmStatus):
    try:
        pmData = {
            **dict(pmStatus),
            'poleId': pole_id,
            'timestamp': datetime.timestamp(datetime.now())
        }
        _id = pmDb.insert_one(pmData).inserted_id
        pmData['_id'] = str(_id)
        return {
        'message': 'created succesfully',
          'data': pmData
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")
