"""
Reusable Agent Skills Library Management Package.
Provides modules for intake scanning, validation, canonical updates,
runtime symlink synchronization, and audit logging.
"""

__version__ = "1.0.0"

from .object_model import (
    CanonicalIdentity,
    CanonicalIdentityError,
    SkillRole,
    RelationshipType,
    Relationship,
    SkillObject,
    CapabilityObject,
    WorkflowObject,
    FamilyObject,
    PrimitiveObject,
    OverlayObject,
    AdapterObject,
    AliasObject,
    ReferenceObject,
    RouterObject,
    GeneratedArtifactObject,
    ObjectGraph,
    InvariantViolationError,
)
