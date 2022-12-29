from fastapi import APIRouter, Depends, HTTPException

from config.db import poleDb, pmDb
from models.light import LightStatus, LightingPole
from bson import ObjectId
from models.user import User
from schemas.user import get_current_active_user

from schemas.utils import serializeDict, serializeList

light = APIRouter(prefix='/light')

@light.get('/')
async def find_all_pole():
    try:
        return serializeList(poleDb.find())
    except:
        raise HTTPException(status_code=400, detail="some error")

@light.get('/{pole_id}')
async def find_one_pole(pole_id):
    try:
        poleData = serializeDict(poleDb.find_one({"_id":ObjectId(pole_id)}))
        try:
            poleData['pm'] = serializeDict(pmDb.find({"poleId":pole_id}).limit(1).sort([('$natural',-1)])[0])
        except:
            pass
        return poleData
    except:
        raise HTTPException(status_code=400, detail="pole with the provided id could not be found")

@light.post('/')
async def create_pole(lightingPole: LightingPole):
    try:
        lightData = dict(lightingPole)
        _id = poleDb.insert_one(lightData).inserted_id
        lightData['_id'] = str(_id)
        return {
          'message': 'created succesfully',
          'data': lightData
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")

@light.patch('/pole/{pole_id}')
async def update_pole(pole_id: str,lightPole : LightingPole):
    try: 
        poleDb.update_one({"_id": ObjectId(pole_id)},{ '$set' :dict(lightPole)})
        return {
          'message': 'updated succesfully',
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")

@light.delete('/pole/{pole_id}')
async def delete_pole(pole_id: str):
    try: 
        poleDb.delete_one({"_id": ObjectId(pole_id)})
        return {
          'message': 'delete succesfully',
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")

@light.patch('/{pole_id}')
async def update_light_status(pole_id: str,lightStatus : LightStatus):
    try: 
        poleDb.update_one({"_id": ObjectId(pole_id)},{ '$set' :dict(lightStatus)})
        return {
          'message': 'updated succesfully',
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="wrong format")
    
@light.patch("/toggle/{pole_id}")
async def toggle_light_by_admin(pole_id,current_user: User = Depends(get_current_active_user)):
    print(current_user)
    if(current_user.permission < 0):
        raise HTTPException(status_code=403, detail="no permission")
    try:
        poleData = poleDb.find_one({"_id":ObjectId(pole_id)})
        if not poleData:
            raise Exception('error')
        if poleData['status']:
            poleData['status'] = 0
        else:
            poleData['status'] = 1
        poleDb.update_one({"_id":ObjectId(pole_id)},{'$set': poleData})
        return {
            'message': 'update successfully'
        }
    except:
        raise HTTPException(status_code=400, detail="could find pole")
