"""
Graph Builder for Neo4j
Manages knowledge graph construction and queries.
"""

from typing import List, Dict, Any, Optional

from neo4j import GraphDatabase, Driver
from loguru import logger

from app.config import get_settings
from app.services.graph.entity_extractor import Entity, Relationship, GraphData


class GraphBuilder:
    """
    Builds and manages knowledge graph in Neo4j.
    """

    def __init__(self, driver: Optional[Driver] = None):
        """
        Initialize graph builder.

        Args:
            driver: Optional Neo4j driver instance
        """
        self.settings = get_settings()

        if driver:
            self.driver = driver
        else:
            self.driver = GraphDatabase.driver(
                self.settings.neo4j_uri,
                auth=(self.settings.neo4j_user, self.settings.neo4j_password)
            )

        self._init_constraints()
        logger.info("Initialized graph builder")

    def close(self) -> None:
        """
        Close the Neo4j driver connection.
        """
        self.driver.close()

    def _init_constraints(self) -> None:
        """
        Initialize database constraints and indexes.
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            constraints = [
                "CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
                "CREATE INDEX concept_subject IF NOT EXISTS FOR (c:Concept) ON (c.subject)",
                "CREATE INDEX concept_difficulty IF NOT EXISTS FOR (c:Concept) ON (c.difficulty)",
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    # Constraint might already exist
                    logger.debug(f"Constraint creation info: {str(e)}")

        logger.info("Initialized constraints and indexes")

    def add_graph_data(self, graph_data: GraphData) -> Dict[str, int]:
        """
        Add entities and relationships to the graph.

        Args:
            graph_data: Graph data with entities and relationships

        Returns:
            Dictionary with counts of created nodes and relationships
        """
        nodes_created = self.add_entities_batch(graph_data.entities)
        rels_created = self.add_relationships_batch(graph_data.relationships)

        return {
            "nodes_created": nodes_created,
            "relationships_created": rels_created
        }

    def add_entities_batch(self, entities: List[Entity]) -> int:
        """
        Batch add entities to the graph.

        Args:
            entities: List of entities to add

        Returns:
            Number of nodes created/updated
        """
        if not entities:
            return 0

        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            UNWIND $entities AS entity
            CALL apoc.merge.node(
                [entity.type],
                {name: entity.name},
                entity.properties,
                entity.properties
            ) YIELD node
            SET node.description = entity.description
            RETURN count(node) as created
            """

            # Convert entities to dicts
            entities_data = [
                {
                    "type": entity.type,
                    "name": entity.name,
                    "description": entity.description,
                    "properties": entity.properties
                }
                for entity in entities
            ]

            try:
                result = session.run(query, entities=entities_data)
                count = result.single()["created"]
                logger.info(f"Created/updated {count} nodes")
                return count
            except Exception as e:
                logger.error(f"Error adding entities: {str(e)}")
                # Fallback: add one by one
                return self._add_entities_individually(session, entities)

    def _add_entities_individually(self, session, entities: List[Entity]) -> int:
        """
        Fallback method to add entities one by one (if APOC is not available).

        Args:
            session: Neo4j session
            entities: List of entities

        Returns:
            Number of entities added
        """
        count = 0
        for entity in entities:
            try:
                query = f"""
                MERGE (n:{entity.type} {{name: $name}})
                SET n.description = $description,
                    n += $properties
                RETURN n
                """

                session.run(
                    query,
                    name=entity.name,
                    description=entity.description,
                    properties=entity.properties
                )
                count += 1
            except Exception as e:
                logger.error(f"Error adding entity {entity.name}: {str(e)}")

        return count

    def add_relationships_batch(self, relationships: List[Relationship]) -> int:
        """
        Batch add relationships to the graph.

        Args:
            relationships: List of relationships to add

        Returns:
            Number of relationships created
        """
        if not relationships:
            return 0

        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            UNWIND $relationships AS rel
            MATCH (source {name: rel.source})
            MATCH (target {name: rel.target})
            CALL apoc.merge.relationship(
                source,
                rel.type,
                {},
                rel.properties,
                target
            ) YIELD rel as relationship
            RETURN count(relationship) as created
            """

            # Convert relationships to dicts
            rels_data = [
                {
                    "source": rel.source,
                    "target": rel.target,
                    "type": rel.type,
                    "properties": rel.properties
                }
                for rel in relationships
            ]

            try:
                result = session.run(query, relationships=rels_data)
                count = result.single()["created"]
                logger.info(f"Created {count} relationships")
                return count
            except Exception as e:
                logger.error(f"Error adding relationships: {str(e)}")
                # Fallback
                return self._add_relationships_individually(session, relationships)

    def _add_relationships_individually(
        self,
        session,
        relationships: List[Relationship]
    ) -> int:
        """
        Fallback method to add relationships one by one.

        Args:
            session: Neo4j session
            relationships: List of relationships

        Returns:
            Number of relationships added
        """
        count = 0
        for rel in relationships:
            try:
                query = f"""
                MATCH (source {{name: $source}})
                MATCH (target {{name: $target}})
                MERGE (source)-[r:{rel.type}]->(target)
                SET r += $properties
                RETURN r
                """

                result = session.run(
                    query,
                    source=rel.source,
                    target=rel.target,
                    properties=rel.properties
                )

                if result.single():
                    count += 1

            except Exception as e:
                logger.error(f"Error adding relationship {rel.source}->{rel.target}: {str(e)}")

        return count

    def get_all_concepts(self, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all concepts in the graph.

        Args:
            subject: Optional subject filter

        Returns:
            List of concepts
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            if subject:
                query = """
                MATCH (c:Concept)
                WHERE c.subject = $subject
                RETURN c.name as name, c.description as description,
                       c.difficulty as difficulty, labels(c) as labels
                ORDER BY c.name
                """
                result = session.run(query, subject=subject)
            else:
                query = """
                MATCH (c:Concept)
                RETURN c.name as name, c.description as description,
                       c.difficulty as difficulty, labels(c) as labels
                ORDER BY c.name
                """
                result = session.run(query)

            return [dict(record) for record in result]

    def get_concept(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific concept by name.

        Args:
            name: Concept name

        Returns:
            Concept data or None
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            MATCH (c:Concept {name: $name})
            RETURN c.name as name, c.description as description,
                   c.difficulty as difficulty, properties(c) as properties
            """

            result = session.run(query, name=name)
            record = result.single()

            return dict(record) if record else None

    def get_stats(self) -> Dict[str, Any]:
        """
        Get graph statistics.

        Returns:
            Statistics dictionary
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            MATCH (n)
            OPTIONAL MATCH ()-[r]->()
            RETURN
                count(DISTINCT n) as total_nodes,
                count(DISTINCT r) as total_relationships,
                count(DISTINCT CASE WHEN 'Concept' IN labels(n) THEN n END) as concepts,
                count(DISTINCT CASE WHEN 'Topic' IN labels(n) THEN n END) as topics,
                count(DISTINCT CASE WHEN 'Person' IN labels(n) THEN n END) as people
            """

            result = session.run(query)
            return dict(result.single())

    def delete_all(self) -> None:
        """
        Delete all nodes and relationships (use with caution!).
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.warning("Deleted all graph data")


# Global graph builder instance
_graph_builder: Optional[GraphBuilder] = None


def get_graph_builder() -> GraphBuilder:
    """
    Get the global graph builder instance.

    Returns:
        GraphBuilder instance
    """
    global _graph_builder
    if _graph_builder is None:
        _graph_builder = GraphBuilder()
    return _graph_builder
