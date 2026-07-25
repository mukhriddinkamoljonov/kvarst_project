from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

app = FastAPI(title="Kvarts API")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float




class ItemOut(Item):
    id: UUID


items: dict[UUID, Item] = {}


@app.get("/items")
def list_items():
    return [ItemOut(id=id, **item.model_dump()) for id, item in items.items()]


@app.get("/items1")
def list_items1():
    return [ItemOut(id=id, **item.model_dump()) for id, item in items.items()]


@app.post("/items", status_code=201)
def create_item(item: Item):
    id = uuid4()
    items[id] = item
    return ItemOut(id=id, **item.model_dump())


@app.get("/items/{item_id}")
def get_item(item_id: UUID):
    if item_id not in items:
        raise HTTPException(404, "Item not found")
    return ItemOut(id=item_id, **items[item_id].model_dump())


@app.put("/items/{item_id}")
def update_item(item_id: UUID, item: Item):
    if item_id not in items:
        raise HTTPException(404, "Item not found")
    items[item_id] = item
    return ItemOut(id=item_id, **item.model_dump())


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: UUID):
    if item_id not in items:
        raise HTTPException(404, "Item not found")
    del items[item_id]
