"""
Path Finder for Learning Paths
Finds optimal learning paths through the knowledge graph.
"""

from typing import List, Dict, Any, Optional

from neo4j import Driver
from loguru import logger

from app.config import get_settings


class PathFinder:
    """
    Finds optimal learning paths in the knowledge graph.
    """

    def __init__(self, driver: Driver):
        """
        Initialize path finder.

        Args:
            driver: Neo4j driver instance
        """
        self.driver = driver
        self.settings = get_settings()
        logger.info("Initialized path finder")

    def find_learning_path(
        self,
        start_concept: str,
        end_concept: str,
        max_length: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find optimal learning path between two concepts.

        Args:
            start_concept: Starting concept name
            end_concept: Target concept name
            max_length: Maximum path length

        Returns:
            List of paths with metadata
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = f"""
            MATCH path = shortestPath(
                (start:Concept {{name: $start}})-[*..{max_length}]-(end:Concept {{name: $end}})
            )
            WHERE ALL(r IN relationships(path)
                     WHERE type(r) IN ['PREREQUISITE_OF', 'RELATES_TO', 'PART_OF'])
            WITH path,
                 [node IN nodes(path) | node.name] AS concepts,
                 [node IN nodes(path) | coalesce(node.difficulty, 3)] AS difficulties,
                 [node IN nodes(path) | node.description] AS descriptions
            RETURN
                concepts,
                descriptions,
                difficulties,
                reduce(s = 0, d IN difficulties | s + d) AS total_difficulty,
                length(path) AS path_length,
                reduce(s = 0, d IN difficulties | s + d) / length(path) AS avg_difficulty
            ORDER BY path_length ASC, total_difficulty ASC
            LIMIT 5
            """

            result = session.run(query, start=start_concept, end=end_concept)
            paths = []

            for record in result:
                # Estimate hours based on difficulty
                avg_difficulty = record["avg_difficulty"]
                path_length = record["path_length"]
                estimated_hours = path_length * (avg_difficulty * 0.5)  # Rough estimate

                paths.append({
                    "concepts": record["concepts"],
                    "descriptions": record["descriptions"],
                    "difficulties": record["difficulties"],
                    "total_difficulty": record["total_difficulty"],
                    "path_length": path_length,
                    "estimated_hours": round(estimated_hours, 1)
                })

            logger.info(f"Found {len(paths)} paths from {start_concept} to {end_concept}")
            return paths

    def find_related_concepts(
        self,
        concept: str,
        depth: int = 2,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Find related concepts up to specified depth.

        Args:
            concept: Central concept name
            depth: Maximum relationship depth
            limit: Maximum number of nodes to return

        Returns:
            Graph data with nodes and relationships
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = f"""
            MATCH (center:Concept {{name: $concept}})
            CALL apoc.path.subgraphAll(center, {{
                maxLevel: $depth,
                relationshipFilter: 'RELATES_TO|PREREQUISITE_OF|PART_OF',
                limit: $limit
            }})
            YIELD nodes, relationships

            WITH [node IN nodes | {{
                id: id(node),
                name: node.name,
                type: labels(node)[0],
                description: node.description,
                importance: coalesce(node.importance, 0.5),
                difficulty: coalesce(node.difficulty, 3)
            }}] AS nodeData,
            [rel IN relationships | {{
                source: id(startNode(rel)),
                target: id(endNode(rel)),
                type: type(rel),
                weight: coalesce(rel.weight, 1.0)
            }}] AS edgeData

            RETURN nodeData, edgeData
            """

            try:
                result = session.run(query, concept=concept, depth=depth, limit=limit)
                record = result.single()

                if record:
                    return {
                        "nodes": record["nodeData"],
                        "edges": record["edgeData"]
                    }
                else:
                    # Fallback if APOC is not available
                    return self._find_related_concepts_fallback(session, concept, depth)

            except Exception as e:
                logger.warning(f"APOC path finding failed, using fallback: {str(e)}")
                return self._find_related_concepts_fallback(session, concept, depth)

    def _find_related_concepts_fallback(
        self,
        session,
        concept: str,
        depth: int
    ) -> Dict[str, Any]:
        """
        Fallback method without APOC.

        Args:
            session: Neo4j session
            concept: Central concept
            depth: Maximum depth

        Returns:
            Graph data
        """
        query = f"""
        MATCH (center:Concept {{name: $concept}})
        MATCH path = (center)-[*1..{depth}]-(related:Concept)
        WITH DISTINCT related, center, relationships(path) as rels
        LIMIT 50

        WITH collect(DISTINCT {{
            id: id(center),
            name: center.name,
            type: labels(center)[0],
            description: center.description,
            difficulty: coalesce(center.difficulty, 3)
        }}) +
        collect(DISTINCT {{
            id: id(related),
            name: related.name,
            type: labels(related)[0],
            description: related.description,
            difficulty: coalesce(related.difficulty, 3)
        }}) as nodes,
        [r IN rels | {{
            source: id(startNode(r)),
            target: id(endNode(r)),
            type: type(r),
            weight: 1.0
        }}] as edges

        RETURN nodes, edges
        """

        result = session.run(query, concept=concept)
        record = result.single()

        if record:
            return {
                "nodes": record["nodes"],
                "edges": record["edges"]
            }
        else:
            return {"nodes": [], "edges": []}

    def get_prerequisites(self, concept: str) -> List[Dict[str, Any]]:
        """
        Get all prerequisites for a concept.

        Args:
            concept: Concept name

        Returns:
            List of prerequisite concepts
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(concept:Concept {name: $concept})
            RETURN prereq.name as name,
                   prereq.description as description,
                   prereq.difficulty as difficulty
            ORDER BY prereq.difficulty
            """

            result = session.run(query, concept=concept)
            return [dict(record) for record in result]

    def suggest_next_concepts(
        self,
        completed_concepts: List[str],
        subject: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest next concepts to learn based on completed concepts.

        Args:
            completed_concepts: List of completed concept names
            subject: Optional subject filter

        Returns:
            List of suggested concepts with reasons
        """
        with self.driver.session(database=self.settings.neo4j_database) as session:
            query = """
            // Find concepts that have prerequisites satisfied
            MATCH (next:Concept)
            WHERE NOT next.name IN $completed

            OPTIONAL MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(next)
            WITH next, collect(prereq.name) as prerequisites

            WHERE ALL(p IN prerequisites WHERE p IN $completed)
                OR size(prerequisites) = 0

            OPTIONAL MATCH (completed_concept:Concept)-[:RELATES_TO]-(next)
            WHERE completed_concept.name IN $completed
            WITH next, prerequisites, count(completed_concept) as related_count

            RETURN
                next.name as name,
                next.description as description,
                next.difficulty as difficulty,
                prerequisites,
                related_count,
                CASE
                    WHEN size(prerequisites) > 0 THEN 'Has prerequisites met'
                    WHEN related_count > 0 THEN 'Related to completed concepts'
                    ELSE 'New topic'
                END as reason
            ORDER BY related_count DESC, next.difficulty ASC
            LIMIT 10
            """

            result = session.run(query, completed=completed_concepts)
            return [dict(record) for record in result]
