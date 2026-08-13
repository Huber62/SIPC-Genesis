from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProtectionProcedureStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    CC_APPROVED = "cc_approved"
    SUBMITTED_TO_CDS = "submitted_to_cds"
    CDS_APPROVED = "cds_approved"
    IN_FORCE = "in_force"
    REJECTED = "rejected"


class DocumentStatus(str, Enum):
    DRAFT = "draft"
    PROPOSED = "proposed"
    IN_PROCEDURE = "in_procedure"
    IN_FORCE = "in_force"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class DocumentCategory(str, Enum):
    NORMATIVE = "normative"
    PLANNING_PROCEDURE = "planning_procedure"
    PROCEDURAL_ACT = "procedural_act"
    HERITAGE_SHEET = "heritage_sheet"
    TECHNICAL_DOCUMENT = "technical_document"
    PHOTOGRAPHIC_DOCUMENT = "photographic_document"
    PRACTICE_DOCUMENT = "practice_document"
    ECONOMIC_DOCUMENT = "economic_document"
    OTHER = "other"


@dataclass
class HeritageDocument:
    document_id: str
    document_type: str
    title: str
    status: DocumentStatus
    category: DocumentCategory
    file_path: Optional[str] = None
    source: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class HeritageTwin:
    sipc_id: str
    municipality: str
    section: str
    parcel: str
    name: str

    heritage_level: Optional[str] = None
    heritage_status: Optional[str] = None
    heritage_protection_procedure_status: Optional[ProtectionProcedureStatus] = None
    respect_perimeter_procedure_status: Optional[ProtectionProcedureStatus] = None
    protected_now: bool = False
    proposed_for_protection: bool = False

    respect_perimeter_now: bool = False
    proposed_respect_perimeter: bool = False
    documents: list[HeritageDocument] = field(default_factory=list)

