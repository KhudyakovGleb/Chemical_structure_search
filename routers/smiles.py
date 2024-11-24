from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.smile import Smile
from structure_search import substructure_search

router = APIRouter()

SMILES = [
    Smile(id='0001', component="CCO"),
    Smile(id='0002', component="c1ccccc1"),
    Smile(id='0003', component="CC(=O)O"),
    Smile(id='0004', component="CC(=O)Oc1ccccc1C(=O)O"),
]


@router.get("/")
async def list_smiles() -> list[Smile]:
    all_smiles = SMILES
    return all_smiles


@router.get("/{id}")
async def get_smile(id: str) -> Smile:
    for smile in SMILES:
        if id == smile.id:
            return smile
    return JSONResponse(content={"msg": "Not found"}, status_code=404)


@router.get("/search/")
async def get_search_for_smile(substructure: str) -> list:
    components = [smile.component for smile in SMILES]
    return substructure_search(components, substructure)


@router.post("/")
async def create_smile(smile: Smile) -> Smile:
    SMILES.append(smile)
    return smile


@router.put("/{id}")
async def update_smile(id: str, new_smile: Smile) -> Smile:
    for smile in SMILES:
        if id == smile.id:
            smile.component = new_smile.component
            return smile
    else:
        return JSONResponse(content={"msg": "Not found"}, status_code=404)


@router.delete("/{id}")
async def delete_smile(id: str) -> Smile:
    smile_to_remove = None
    for smile in SMILES:
        if id == smile.id:
            smile_to_remove = smile
            break
    else:
        return JSONResponse(content={"msg": "Not found"}, status_code=404)
    SMILES.remove(smile_to_remove)
    return smile_to_remove
