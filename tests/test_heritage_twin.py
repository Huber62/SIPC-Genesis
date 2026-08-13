from backend.app.models.heritage_twin import (
    DocumentCategory,
    DocumentStatus,
    HeritageDocument,
    HeritageTwin,
    ProtectionProcedureStatus,
)


def test_heritage_twin_creation_and_defaults() -> None:
    twin = HeritageTwin(
        sipc_id="SIPC-001",
        municipality="Example Municipality",
        section="A",
        parcel="12",
        name="Villa Example",
    )

    assert twin.sipc_id == "SIPC-001"
    assert twin.municipality == "Example Municipality"
    assert twin.section == "A"
    assert twin.parcel == "12"
    assert twin.name == "Villa Example"

    assert twin.protected_now is False
    assert twin.proposed_for_protection is False
    assert twin.respect_perimeter_now is False
    assert twin.proposed_respect_perimeter is False

    assert twin.heritage_level is None
    assert twin.heritage_status is None
    assert twin.heritage_protection_procedure_status is None
    assert twin.respect_perimeter_procedure_status is None
    assert twin.documents == []


def test_heritage_twin_heritage_protection_procedure_status_proposed() -> None:
    twin = HeritageTwin(
        sipc_id="SIPC-002",
        municipality="Example Municipality",
        section="B",
        parcel="7",
        name="Palazzo Example",
        heritage_protection_procedure_status=ProtectionProcedureStatus.PROPOSED,
    )

    assert twin.heritage_protection_procedure_status is ProtectionProcedureStatus.PROPOSED
    assert twin.heritage_protection_procedure_status == ProtectionProcedureStatus.PROPOSED


def test_heritage_twin_tracks_separate_procedure_statuses() -> None:
    twin = HeritageTwin(
        sipc_id="SIPC-003",
        municipality="Example Municipality",
        section="C",
        parcel="21",
        name="Villa Separate Status",
        heritage_protection_procedure_status=ProtectionProcedureStatus.CC_APPROVED,
        respect_perimeter_procedure_status=ProtectionProcedureStatus.PROPOSED,
    )

    assert twin.heritage_protection_procedure_status is ProtectionProcedureStatus.CC_APPROVED
    assert twin.respect_perimeter_procedure_status is ProtectionProcedureStatus.PROPOSED
    assert twin.heritage_protection_procedure_status != twin.respect_perimeter_procedure_status


def test_heritage_twin_can_store_documents_with_different_statuses() -> None:
    napr_document = HeritageDocument(
        document_id="NAPR-001",
        document_type="NAPR",
        title="Current NAPR",
        status=DocumentStatus.IN_FORCE,
        category=DocumentCategory.NORMATIVE,
        file_path="/docs/napr.pdf",
        source="municipality",
    )
    heritage_sheet = HeritageDocument(
        document_id="HS-010",
        document_type="scheda UBC",
        title="Proposed heritage sheet",
        status=DocumentStatus.PROPOSED,
        category=DocumentCategory.HERITAGE_SHEET,
        file_path="/docs/heritage_sheet.pdf",
        source="cadastre",
    )

    twin = HeritageTwin(
        sipc_id="SIPC-004",
        municipality="Example Municipality",
        section="D",
        parcel="42",
        name="Villa Documents",
        documents=[napr_document, heritage_sheet],
    )

    assert len(twin.documents) == 2
    assert twin.documents[0].status is DocumentStatus.IN_FORCE
    assert twin.documents[1].status is DocumentStatus.PROPOSED
    assert twin.documents[0].document_type == "NAPR"
    assert twin.documents[1].document_type == "scheda UBC"
    assert twin.documents[0].category is DocumentCategory.NORMATIVE
    assert twin.documents[1].category is DocumentCategory.HERITAGE_SHEET
    assert twin.documents[0].status != twin.documents[1].status
    assert twin.documents[0].category != twin.documents[1].category


def test_heritage_twin_realistic_sipc_case_study() -> None:
    related_parcels = ["1988", "2041"]

    twin = HeritageTwin(
        sipc_id="SIPC-COLINA-1988-2041",
        municipality="Collina d'Oro",
        section="Montagnola",
        parcel="1988",
        name="Villa di Montagnola",
        protected_now=False,
        proposed_for_protection=True,
        heritage_protection_procedure_status=ProtectionProcedureStatus.PROPOSED,
        respect_perimeter_now=False,
        proposed_respect_perimeter=True,
        respect_perimeter_procedure_status=ProtectionProcedureStatus.PROPOSED,
        documents=[
            HeritageDocument(
                document_id="NAPR-001",
                document_type="NAPR",
                title="Current NAPR",
                status=DocumentStatus.IN_FORCE,
                category=DocumentCategory.NORMATIVE,
                file_path="/docs/napr.pdf",
                source="municipality",
            ),
            HeritageDocument(
                document_id="HS-010",
                document_type="scheda bene culturale",
                title="Proposed heritage sheet",
                status=DocumentStatus.PROPOSED,
                category=DocumentCategory.HERITAGE_SHEET,
                file_path="/docs/heritage_sheet.pdf",
                source="cadastre",
            ),
            HeritageDocument(
                document_id="PR-044",
                document_type="variante PR tutela beni culturali",
                title="Planning procedure document",
                status=DocumentStatus.IN_PROCEDURE,
                category=DocumentCategory.PLANNING_PROCEDURE,
                file_path="/docs/planning_procedure.pdf",
                source="municipality",
            ),
        ],
    )

    assert twin.municipality == "Collina d'Oro"
    assert twin.section == "Montagnola"
    assert twin.parcel == "1988"
    assert related_parcels == ["1988", "2041"]
    assert twin.protected_now is False
    assert twin.proposed_for_protection is True
    assert twin.heritage_protection_procedure_status is ProtectionProcedureStatus.PROPOSED
    assert twin.respect_perimeter_now is False
    assert twin.proposed_respect_perimeter is True
    assert twin.respect_perimeter_procedure_status is ProtectionProcedureStatus.PROPOSED

    assert len(twin.documents) == 3

    assert twin.documents[0].category is DocumentCategory.NORMATIVE
    assert twin.documents[0].document_type == "NAPR"
    assert twin.documents[0].status is DocumentStatus.IN_FORCE

    assert twin.documents[1].category is DocumentCategory.HERITAGE_SHEET
    assert twin.documents[1].document_type == "scheda bene culturale"
    assert twin.documents[1].status is DocumentStatus.PROPOSED

    assert twin.documents[2].category is DocumentCategory.PLANNING_PROCEDURE
    assert twin.documents[2].document_type == "variante PR tutela beni culturali"
    assert twin.documents[2].status is DocumentStatus.IN_PROCEDURE
