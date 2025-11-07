# Knowledge Graph - Analyse und Nutzung

## Aktueller Stand (v2.0)

### Was der Knowledge Graph JETZT macht:

1. **Visualisierung von Konzepten**
   - Zeigt Konzepte, Topics und Personen aus Dokumenten
   - Visualisiert Beziehungen zwischen Entitäten
   - Interaktive Cytoscape.js Darstellung
   - Zoom, Pan, Suche möglich

2. **Automatische Entity Extraction**
   - Beim Dokumenten-Upload werden automatisch Konzepte extrahiert
   - Nutzt OpenAI GPT-4o-mini für intelligente Erkennung
   - Speichert Entities in Neo4j Graph Database

3. **Path Finding**
   - Kann Verbindungen zwischen Konzepten finden
   - Zeigt wie Konzepte miteinander zusammenhängen

### Was der Knowledge Graph NICHT macht:

❌ **Der Graph wird NICHT für RAG-Queries genutzt**

Der RAG Chain (`backend/app/services/rag/rag_chain.py`) nutzt aktuell:
- ✅ Vector Store (ChromaDB) für semantische Suche
- ✅ OpenAI Embeddings für Ähnlichkeitssuche
- ✅ LangChain ConversationalRetrievalChain

Aber:
- ❌ Keine Integration mit Neo4j Graph
- ❌ Keine Graph-basierte Kontexterweiterung
- ❌ Keine Konzept-Beziehungen in Antworten

## Mögliche Erweiterungen

### Option 1: Graph-Enhanced RAG (Hybrid Approach)

**Idee**: Nutze sowohl Vector Store ALS AUCH Knowledge Graph

**Workflow**:
```
1. User stellt Frage
2. Vector Store findet relevante Dokument-Chunks (wie jetzt)
3. NEU: Extrahiere Konzepte aus Chunks
4. NEU: Frage Neo4j nach verwandten Konzepten
5. NEU: Erweitere Kontext mit Graph-Beziehungen
6. LLM generiert Antwort mit erweitertem Kontext
```

**Vorteile**:
- Besseres Verständnis von Zusammenhängen
- Kann Konzepte aus verschiedenen Dokumenten verbinden
- Zeigt "hidden connections" die nicht direkt im Text stehen

**Nachteile**:
- Komplexere Implementierung
- Langsamere Queries
- Mehr API Calls (OpenAI)

### Option 2: Graph-Only Queries (Alternative Query Mode)

**Idee**: Spezieller "Konzept-Modus" der nur den Graph nutzt

**Beispiel-Fragen**:
- "Wie hängt Konzept A mit Konzept B zusammen?"
- "Zeige mir alle Konzepte zum Thema X"
- "Was sind die Hauptthemen in meinen Dokumenten?"

**Implementation**:
- Neuer Endpoint: `/api/rag/query-graph`
- Fragt Neo4j direkt ab
- Nutzt Cypher Queries für strukturierte Antworten

## Empfehlung für v2.1

**Für die meisten Studierenden ist der aktuelle Ansatz optimal:**

✅ **RAG (Vector Store)**: Beste Antworten auf spezifische Fragen
✅ **Knowledge Graph**: Visualisierung zum "großen Bild" sehen

**Der Graph ist wertvoll für**:
1. Überblick über alle Themen
2. Entdecken von Zusammenhängen
3. Navigation durch komplexe Inhalte
4. Vorbereitung auf mündliche Prüfungen

**RAG ist optimal für**:
1. Spezifische Fragen beantworten
2. Zitate und Quellenangaben
3. Detaillierte Erklärungen
4. Schnelle Antworten

## Technische Details

### Aktuell genutzte Komponenten:

**Vector Store (ChromaDB)**:
- Embeddings: `text-embedding-3-small`
- Chunk Size: 1000 Zeichen
- Overlap: 200 Zeichen
- Top-K Retrieval: 4 Chunks

**Knowledge Graph (Neo4j)**:
- Node Types: Concept, Topic, Person
- Relationships: RELATES_TO, PART_OF, MENTIONS
- Constraints: Unique names per type
- Indexes: subject, difficulty

**Entity Extraction**:
- Model: GPT-4o-mini
- Structured Output: Ja (Pydantic models)
- Batch Processing: Ja

### Mögliche Graph-RAG Integration (Pseudocode):

```python
def graph_enhanced_query(question: str) -> Dict:
    # 1. Standard RAG Retrieval
    chunks = vector_store.similarity_search(question, k=4)

    # 2. Extract concepts from retrieved chunks
    concepts = extract_concepts_from_chunks(chunks)

    # 3. Query graph for related concepts
    related = graph.get_related_concepts(concepts, depth=2)

    # 4. Get context from related concepts
    extended_context = get_concept_descriptions(related)

    # 5. Combine all context
    full_context = chunks + extended_context

    # 6. Generate answer
    answer = llm.generate(question, full_context)

    return {
        "answer": answer,
        "sources": format_sources(chunks),
        "related_concepts": related  # NEU!
    }
```

## Fazit

**Aktuelle Situation**: Der Knowledge Graph ist primär ein Visualisierungstool.

**Das ist vollkommen in Ordnung!** Die Trennung ermöglicht:
- Schnelle RAG-Queries (kein Graph-Overhead)
- Flexible Graph-Visualisierung
- Einfache Wartung

**Für 90% der Use-Cases reicht die aktuelle Implementation.**

Wenn Du erweiterte Graph-RAG Features willst, können wir diese als **v2.1 Feature** implementieren mit einem separaten Endpoint, sodass User wählen können:
- `/api/rag/query` → Schnell, Vector-basiert (Standard)
- `/api/rag/query-enhanced` → Langsamer, Graph-enhanced (Optional)

---

**Dokumentiert am: 2025-11-07**
**Version: v2.0**
**Status**: ✅ Produktiv, funktional, optimiert für lokale Nutzung
