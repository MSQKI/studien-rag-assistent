"""
Entity Extractor for Knowledge Graph
Uses LLM to extract entities and relationships from text.
"""

import json
from typing import List, Dict, Any
from fuzzywuzzy import fuzz

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from loguru import logger

from app.config import get_settings


class Entity(BaseModel):
    """Represents an entity (concept, person, etc.)"""
    name: str
    type: str  # Concept, Person, Topic, Resource
    description: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class Relationship(BaseModel):
    """Represents a relationship between entities"""
    source: str
    target: str
    type: str  # PREREQUISITE_OF, RELATES_TO, PART_OF, TAUGHT_BY
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphData(BaseModel):
    """Graph data with entities and relationships"""
    entities: List[Entity]
    relationships: List[Relationship]


class EntityExtractor:
    """
    Extracts entities and relationships from academic text using LLM.
    """

    def __init__(self):
        """
        Initialize entity extractor.
        """
        self.settings = get_settings()
        self.llm = ChatOpenAI(
            model=self.settings.llm_model,
            temperature=0.1,  # Low temperature for consistent extraction
            openai_api_key=self.settings.openai_api_key
        )
        self.parser = PydanticOutputParser(pydantic_object=GraphData)
        self._init_prompt()
        logger.info("Initialized entity extractor")

    def _init_prompt(self) -> None:
        """
        Initialize extraction prompt template.
        """
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Du bist ein Experte für Wissensextraktion aus akademischen Texten.

Deine Aufgabe ist es, Entitäten und Beziehungen zu extrahieren und als strukturiertes Wissensgraph-Schema zurückzugeben.

**Entitäten-Typen:**
- **Concept**: Fachbegriffe, Theorien, Methoden, Algorithmen, Konzepte
- **Person**: Forscher, Autoren, historische Figuren
- **Topic**: Übergeordnete Themen, Kapitel, Fachgebiete
- **Resource**: Bücher, Papers, Websites, Tools

**Beziehungs-Typen:**
- **PREREQUISITE_OF**: A ist Voraussetzung für B (A muss vor B verstanden werden)
- **RELATES_TO**: A steht in thematischer Beziehung zu B
- **PART_OF**: A ist Teil von B (hierarchisch)
- **TAUGHT_BY**: A wird gelehrt/entwickelt von B (Person)
- **MENTIONED_IN**: A wird erwähnt in B (Resource)

**Wichtige Regeln:**
1. Extrahiere nur die wichtigsten, zentralen Konzepte
2. Beschreibungen sollten präzise und informativ sein
3. Verwende deutsche Namen für deutsche Texte
4. Achte auf korrekte Beziehungsrichtungen
5. Füge relevante Properties hinzu (z.B. difficulty, importance)

{format_instructions}"""),
            ("user", "**Text:**\n{text}\n\n**Fachgebiet (optional):** {subject}")
        ])

    def extract(
        self,
        text: str,
        subject: str | None = None,
        chunk_metadata: Dict[str, Any] | None = None
    ) -> GraphData:
        """
        Extract entities and relationships from text.

        Args:
            text: Text to extract from
            subject: Optional subject area
            chunk_metadata: Optional metadata (page number, source, etc.)

        Returns:
            GraphData with entities and relationships
        """
        try:
            messages = self.prompt.format_messages(
                text=text,
                subject=subject or "Allgemein",
                format_instructions=self.parser.get_format_instructions()
            )

            response = self.llm.invoke(messages)

            # Parse the response
            graph_data = self.parser.parse(response.content)

            # Add metadata to properties
            if chunk_metadata:
                for entity in graph_data.entities:
                    entity.properties["source_page"] = chunk_metadata.get("page")
                    entity.properties["source_file"] = chunk_metadata.get("source_file")

                for rel in graph_data.relationships:
                    rel.properties["source_page"] = chunk_metadata.get("page")
                    rel.properties["source_file"] = chunk_metadata.get("source_file")

            logger.info(f"Extracted {len(graph_data.entities)} entities and {len(graph_data.relationships)} relationships")
            return graph_data

        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            # Return empty graph data on error
            return GraphData(entities=[], relationships=[])

    def resolve_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Resolve duplicate entities using fuzzy matching.

        Args:
            entities: List of entities to resolve

        Returns:
            List of unique entities with merged properties
        """
        if not entities:
            return []

        resolved = []
        seen_names = {}

        for entity in entities:
            # Check for similar names
            matched = False

            for idx, existing_name in seen_names.items():
                # Fuzzy match within same type
                if (entity.type == resolved[idx].type and
                    fuzz.ratio(entity.name.lower(), existing_name.lower()) > 85):

                    # Merge properties
                    resolved[idx].properties.update(entity.properties)

                    # Use longer description if available
                    if len(entity.description) > len(resolved[idx].description):
                        resolved[idx].description = entity.description

                    matched = True
                    break

            if not matched:
                resolved.append(entity)
                seen_names[len(resolved) - 1] = entity.name.lower()

        logger.info(f"Resolved {len(entities)} entities to {len(resolved)} unique entities")
        return resolved

    def extract_from_document_chunks(
        self,
        chunks: List[Dict[str, Any]],
        subject: str | None = None
    ) -> GraphData:
        """
        Extract entities from multiple document chunks and merge results.

        Args:
            chunks: List of text chunks with metadata
            subject: Optional subject area

        Returns:
            Merged graph data
        """
        all_entities = []
        all_relationships = []

        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")

            text = chunk.get("text", "")
            metadata = chunk.get("metadata", {})

            if not text.strip():
                continue

            # Extract from this chunk
            graph_data = self.extract(text, subject, metadata)

            all_entities.extend(graph_data.entities)
            all_relationships.extend(graph_data.relationships)

        # Resolve duplicate entities
        unique_entities = self.resolve_entities(all_entities)

        # Deduplicate relationships
        unique_relationships = self._deduplicate_relationships(all_relationships)

        return GraphData(
            entities=unique_entities,
            relationships=unique_relationships
        )

    def _deduplicate_relationships(
        self,
        relationships: List[Relationship]
    ) -> List[Relationship]:
        """
        Remove duplicate relationships.

        Args:
            relationships: List of relationships

        Returns:
            List of unique relationships
        """
        seen = set()
        unique = []

        for rel in relationships:
            # Create a key for this relationship
            key = (rel.source.lower(), rel.target.lower(), rel.type)

            if key not in seen:
                seen.add(key)
                unique.append(rel)

        logger.info(f"Deduplicated {len(relationships)} relationships to {len(unique)} unique")
        return unique
