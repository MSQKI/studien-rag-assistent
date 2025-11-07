"""
Knowledge Graph API Routes
Endpoints for graph visualization and learning path generation.
"""

from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from loguru import logger

from app.config import get_settings, Settings
from app.api.dependencies import get_graph_builder
from app.services.graph.graph_builder import GraphBuilder

router = APIRouter()


# Request/Response Models
class ConceptNode(BaseModel):
    name: str
    type: str
    description: str | None = None
    properties: Dict[str, Any] = {}


class Relationship(BaseModel):
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = {}


class GraphData(BaseModel):
    nodes: List[ConceptNode]
    edges: List[Relationship]


class LearningPath(BaseModel):
    start_concept: str
    end_concept: str
    path: List[str]
    total_difficulty: float
    estimated_hours: float


class ExtractRequest(BaseModel):
    document_id: str
    text: str


@router.post("/extract")
async def extract_entities(
    request: ExtractRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Extract entities and relationships from text.

    Args:
        request: Document text for entity extraction
        settings: Application settings

    Returns:
        Extracted entities and relationships
    """
    # TODO: Implement entity extraction
    raise HTTPException(
        status_code=501,
        detail="Entity extraction not yet implemented"
    )


@router.get("/concepts", response_model=List[ConceptNode])
async def list_concepts(
    subject: str | None = Query(None, description="Filter by subject"),
    graph_builder: GraphBuilder = Depends(get_graph_builder)
):
    """
    List all concepts in the knowledge graph.

    Args:
        subject: Optional subject filter
        graph_builder: Graph builder instance

    Returns:
        List of concept nodes
    """
    try:
        concepts = graph_builder.get_all_concepts(subject=subject)
        return [
            ConceptNode(
                name=concept["name"],
                type=concept["labels"][0] if concept["labels"] else "Concept",
                description=concept.get("description"),
                properties={}
            )
            for concept in concepts
        ]
    except Exception as e:
        logger.error(f"Error listing concepts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/concept/{name}", response_model=ConceptNode)
async def get_concept(
    name: str,
    graph_builder: GraphBuilder = Depends(get_graph_builder)
):
    """
    Get details for a specific concept.

    Args:
        name: Concept name
        graph_builder: Graph builder instance

    Returns:
        Concept node with details
    """
    try:
        concept = graph_builder.get_concept(name)
        if not concept:
            raise HTTPException(
                status_code=404,
                detail=f"Concept '{name}' not found"
            )

        return ConceptNode(
            name=concept["name"],
            type="Concept",
            description=concept.get("description"),
            properties=concept.get("properties", {})
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting concept: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/path", response_model=LearningPath)
async def find_learning_path(
    start: str = Query(..., description="Start concept"),
    end: str = Query(..., description="End concept"),
    max_length: int = Query(10, description="Maximum path length"),
    settings: Settings = Depends(get_settings)
):
    """
    Find optimal learning path between two concepts.

    Args:
        start: Starting concept name
        end: Target concept name
        max_length: Maximum path length
        settings: Application settings

    Returns:
        Optimal learning path
    """
    # TODO: Implement path finding with Neo4j
    raise HTTPException(
        status_code=501,
        detail="Learning path finding not yet implemented"
    )


@router.get("/related/{concept}", response_model=GraphData)
async def get_related_concepts(
    concept: str,
    depth: int = Query(2, ge=1, le=5, description="Relationship depth"),
    settings: Settings = Depends(get_settings)
):
    """
    Get related concepts up to specified depth.

    Args:
        concept: Central concept name
        depth: Maximum relationship depth
        settings: Application settings

    Returns:
        Graph data with related concepts
    """
    # TODO: Implement related concepts query
    return GraphData(nodes=[], edges=[])


@router.get("/stats")
async def get_graph_stats(
    graph_builder: GraphBuilder = Depends(get_graph_builder)
):
    """
    Get knowledge graph statistics.

    Args:
        graph_builder: Graph builder instance

    Returns:
        Graph statistics
    """
    try:
        stats = graph_builder.get_stats()
        return {
            "total_nodes": stats.get("total_nodes", 0),
            "total_relationships": stats.get("total_relationships", 0),
            "concepts": stats.get("concepts", 0),
            "topics": stats.get("topics", 0),
            "people": stats.get("people", 0)
        }
    except Exception as e:
        logger.error(f"Error getting graph stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_graph(
    graph_builder: GraphBuilder = Depends(get_graph_builder)
):
    """
    Clear all graph data (use with caution!).

    Args:
        graph_builder: Graph builder instance

    Returns:
        Deletion confirmation
    """
    try:
        result = graph_builder.delete_all()
        return {
            "message": "Graph data cleared successfully",
            "nodes_deleted": result["nodes_deleted"],
            "relationships_deleted": result["relationships_deleted"]
        }
    except Exception as e:
        logger.error(f"Error clearing graph: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
