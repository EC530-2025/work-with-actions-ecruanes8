
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import streamlit as st
import pandas as pd
import numpy as np
import requests


app = FastAPI()



class Device(BaseModel):
    device_id : str
    name : str 
    room_id : str 
    device_type : str
    status : str

class Room(BaseModel): 
    room_id : str
    name : str 
    house_id : str 
    devices : list[Device] = []

class User(BaseModel): 
    id : int  
    name : str
    email : str
    password : str
    
class House(BaseModel): 
    house_id : str
    name : str 
    address : str
    owner_id : str 
    rooms : list[Room] =[] 

users = []
houses = []
rooms = []
devices = []

#USER FUNCTIONS  
@app.post("/users/", response_model = User)
async def create_user(user: User) :
    users.append(user)
    print("Current users: ", users)
    return user 
@app.get("/users/{user_id}",response_model = User)
async def get_user(user_id: int) :
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code = 404, detail = "User not found")

#HOUSE FUNCTIONS
@app.post("/houses/", response_model = House)
async def create_house(house: House) :
    houses.append(house)
    return house
@app.get("/houses/{house_id}",response_model = House)
async def get_house(house_id: str) :
    for house in houses:
        if house.house_id == house_id:
            return house
    raise HTTPException(status_code = 404, detail = "House not found")
#ROOM FUNCTIONS
@app.post("/rooms/", response_model = Room)
async def create_room(room: Room) :
    rooms.append(room)
    return room
@app.get("/rooms/{room_id}",response_model = Room)
async def get_room(room_id: str) :
    for room in rooms:
        if room.room_id == room_id:
            return room
    raise HTTPException(status_code = 404, detail = "Room not found")
#DEVICE FUNCTIONS
@app.post("/devices/", response_model = Device) 
async def create_device(device: Device) :
    devices.append(device)
    return device
@app.get("/devices/{device_id}",response_model = Device)
async def get_device(device_id: str) :
    for device in devices:
        if device.device_id == device_id:
            return device
    raise HTTPException(status_code = 404, detail = "Device not found")
