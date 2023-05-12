from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from spiffworkflow_backend.models.bpmn_process_definition import BpmnProcessDefinitionModel
from spiffworkflow_backend.models.db import db
from spiffworkflow_backend.models.db import SpiffworkflowBaseDBModel


class BpmnProcessNotFoundError(Exception):
    pass


# properties_json attributes:
#   "last_task", # guid generated by spiff
#   "root", # guid generated by spiff
#   "success", # boolean
#   "bpmn_messages", # if top-level process
#   "correlations", # if top-level process
@dataclass
class BpmnProcessModel(SpiffworkflowBaseDBModel):
    __tablename__ = "bpmn_process"
    id: int = db.Column(db.Integer, primary_key=True)
    guid: str | None = db.Column(db.String(36), nullable=True, unique=True)

    bpmn_process_definition_id: int = db.Column(
        ForeignKey(BpmnProcessDefinitionModel.id), nullable=False, index=True  # type: ignore
    )
    bpmn_process_definition = relationship(BpmnProcessDefinitionModel)

    top_level_process_id: int | None = db.Column(ForeignKey("bpmn_process.id"), nullable=True, index=True)
    direct_parent_process_id: int | None = db.Column(ForeignKey("bpmn_process.id"), nullable=True, index=True)

    properties_json: dict = db.Column(db.JSON, nullable=False)
    json_data_hash: str = db.Column(db.String(255), nullable=False, index=True)

    tasks = relationship("TaskModel", back_populates="bpmn_process", cascade="delete")  # type: ignore
    child_processes = relationship("BpmnProcessModel", foreign_keys=[direct_parent_process_id], cascade="all")

    # FIXME: find out how to set this but it'd be cool
    start_in_seconds: float = db.Column(db.DECIMAL(17, 6))
    end_in_seconds: float | None = db.Column(db.DECIMAL(17, 6))
