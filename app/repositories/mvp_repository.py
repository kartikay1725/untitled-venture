from sqlalchemy.orm import Session
from .models.mvp_blueprint import MVPBlueprint
from .models.mvp_package import MVPPackage
from uuid import UUID

class MVPRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_blueprint(self, idea_id: UUID, wireframes, features, tech_stack, timeline, pdf_url: str) -> MVPBlueprint:
        blueprint = MVPBlueprint(
            idea_id=idea_id,
            wireframes=wireframes,
            feature_list=features,
            tech_stack=tech_stack,
            timeline=timeline,
            pdf_url=pdf_url
        )
        self.db.add(blueprint)
        self.db.commit()
        self.db.refresh(blueprint)
        return blueprint

    def get_blueprint(self, mvp_id: UUID) -> MVPBlueprint | None:
        return self.db.query(MVPBlueprint).filter(MVPBlueprint.id == mvp_id).first()

    def create_package(self, mvp_id: UUID, zip_url: str) -> MVPPackage:
        package = MVPPackage(mvp_id=mvp_id, zip_url=zip_url)
        self.db.add(package)
        self.db.commit()
        self.db.refresh(package)
        return package

    def get_package(self, mvp_id: UUID) -> MVPPackage | None:
        return self.db.query(MVPPackage).filter(MVPPackage.mvp_id == mvp_id).first()