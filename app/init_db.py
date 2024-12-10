from app.database import SessionLocal
from app.models.smile import Smile


def setup_initial_data():
    """Добавить данные по умолчанию в базу."""
    default_smiles = [
        Smile(id="0001", component="CCO"),
        Smile(id="0002", component="c1ccccc1"),
        Smile(id="0003", component="CC(=O)O"),
        Smile(id="0004", component="CC(=O)Oc1ccccc1C(=O)O"),
    ]
    db = SessionLocal()
    try:
        for smile in default_smiles:
            if not db.query(Smile).filter_by(id=smile.id).first():
                db.add(smile)
        db.commit()
    finally:
        db.close()
