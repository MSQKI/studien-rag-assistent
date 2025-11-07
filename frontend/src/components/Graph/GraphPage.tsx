import React, { useState, useRef, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import CytoscapeComponent from 'react-cytoscapejs';
import Cytoscape from 'cytoscape';
import { Network, Search, ZoomIn, ZoomOut, Maximize2, Info } from 'lucide-react';

import { graphAPI } from '../../services/api';

const GraphPage: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const cyRef = useRef<Cytoscape.Core | null>(null);

  // Fetch graph data from API
  const { data: graphData, isLoading, error, isError } = useQuery({
    queryKey: ['graph-data'],
    queryFn: async () => {
      const data = await graphAPI.getConcepts();
      console.log('Graph data fetched:', data);
      return data;
    },
    retry: 1,
  });

  // Transform graph data to Cytoscape format
  const elements = React.useMemo(() => {
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
      console.log('No graph data to display:', graphData);
      return [];
    }

    console.log(`Transforming ${graphData.nodes.length} nodes and ${graphData.edges?.length || 0} edges`);

    // Create nodes
    const nodes = graphData.nodes.map((node: any) => ({
      data: {
        id: node.name,
        label: node.name,
        type: node.type,
        description: node.description,
      },
    }));

    // Create edges
    const edges = (graphData.edges || []).map((edge: any) => ({
      data: {
        id: `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        label: edge.type,
        type: edge.type,
      },
    }));

    console.log('Generated nodes:', nodes.length, 'edges:', edges.length);

    return [...nodes, ...edges];
  }, [graphData]);

  // Cytoscape stylesheet
  const stylesheet: any[] = [
    {
      selector: 'node',
      style: {
        'background-color': '#3498db',
        label: 'data(label)',
        color: '#fff',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': '12px',
        width: 60,
        height: 60,
        'text-wrap': 'wrap',
        'text-max-width': '80px',
        'border-width': 2,
        'border-color': '#2980b9',
      },
    },
    {
      selector: 'node[type="Topic"]',
      style: {
        'background-color': '#9b59b6',
        'border-color': '#8e44ad',
      },
    },
    {
      selector: 'node[type="Person"]',
      style: {
        'background-color': '#e67e22',
        'border-color': '#d35400',
      },
    },
    {
      selector: 'node:selected',
      style: {
        'background-color': '#2ecc71',
        'border-color': '#27ae60',
        'border-width': 4,
      },
    },
    {
      selector: 'edge',
      style: {
        width: 2,
        'line-color': '#95a5a6',
        'target-arrow-color': '#95a5a6',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        label: 'data(type)',
        'font-size': '10px',
        color: '#7f8c8d',
      },
    },
  ];

  // Cytoscape layout
  const layout = {
    name: 'cose',
    animate: true,
    animationDuration: 500,
    nodeDimensionsIncludeLabels: true,
    fit: true,
    padding: 50,
    randomize: false,
    componentSpacing: 100,
    nodeRepulsion: 400000,
    idealEdgeLength: 100,
    edgeElasticity: 100,
    nestingFactor: 5,
  };

  // Handle node tap
  useEffect(() => {
    if (cyRef.current) {
      cyRef.current.on('tap', 'node', (event) => {
        const node = event.target;
        setSelectedNode(node.data());
      });

      cyRef.current.on('tap', (event) => {
        if (event.target === cyRef.current) {
          setSelectedNode(null);
        }
      });
    }
  }, [cyRef.current]);

  // Zoom controls
  const handleZoomIn = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() * 1.2);
      cyRef.current.center();
    }
  };

  const handleZoomOut = () => {
    if (cyRef.current) {
      cyRef.current.zoom(cyRef.current.zoom() * 0.8);
      cyRef.current.center();
    }
  };

  const handleFitToScreen = () => {
    if (cyRef.current) {
      cyRef.current.fit(undefined, 50);
    }
  };

  // Filter nodes by search term
  useEffect(() => {
    if (cyRef.current && searchTerm) {
      cyRef.current.nodes().forEach((node) => {
        const label = node.data('label').toLowerCase();
        if (label.includes(searchTerm.toLowerCase())) {
          node.style('opacity', 1);
        } else {
          node.style('opacity', 0.2);
        }
      });
    } else if (cyRef.current) {
      cyRef.current.nodes().style('opacity', 1);
    }
  }, [searchTerm]);

  return (
    <div>
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '4px' }}>
            Knowledge Graph
          </h1>
          <p style={{ color: '#666' }}>Visualisiere dein Wissen</p>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <div style={{ position: 'relative' }}>
            <Search
              size={18}
              style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#999' }}
            />
            <input
              type="text"
              className="input"
              placeholder="Konzept suchen..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '40px', width: '250px' }}
            />
          </div>

          <button className="btn btn-secondary" onClick={handleZoomIn} title="Vergrößern">
            <ZoomIn size={18} />
          </button>
          <button className="btn btn-secondary" onClick={handleZoomOut} title="Verkleinern">
            <ZoomOut size={18} />
          </button>
          <button className="btn btn-secondary" onClick={handleFitToScreen} title="An Bildschirm anpassen">
            <Maximize2 size={18} />
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: selectedNode ? '1fr 300px' : '1fr', gap: '20px' }}>
        {/* Graph Visualization */}
        <div className="card" style={{ padding: 0, height: '600px', overflow: 'hidden', position: 'relative' }}>
          {isLoading ? (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <p>Lade Graph...</p>
            </div>
          ) : isError || error ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <p style={{ color: '#e74c3c', marginBottom: '10px' }}>Fehler beim Laden des Graphs</p>
              <p style={{ color: '#999', fontSize: '14px' }}>{error?.toString() || 'Unbekannter Fehler'}</p>
            </div>
          ) : elements.length === 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
              <Network size={64} color="#9b59b6" style={{ marginBottom: '20px' }} />
              <h2 style={{ fontSize: '24px', marginBottom: '12px' }}>Noch keine Konzepte</h2>
              <p style={{ color: '#666' }}>
                Lade Dokumente hoch, um Konzepte zu extrahieren und den Knowledge Graph zu füllen.
              </p>
            </div>
          ) : (
            <CytoscapeComponent
              elements={elements}
              style={{ width: '100%', height: '100%' }}
              stylesheet={stylesheet}
              layout={layout}
              cy={(cy: Cytoscape.Core) => {
                cyRef.current = cy;
              }}
            />
          )}
        </div>

        {/* Node Details Sidebar */}
        {selectedNode && (
          <div className="card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <Info size={20} color="#3498db" />
              <h3 style={{ fontSize: '18px', fontWeight: '600' }}>Details</h3>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ fontSize: '12px', color: '#999', marginBottom: '4px' }}>Konzept</div>
              <div style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>{selectedNode.label}</div>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ fontSize: '12px', color: '#999', marginBottom: '4px' }}>Typ</div>
              <span
                style={{
                  padding: '4px 12px',
                  borderRadius: '12px',
                  backgroundColor:
                    selectedNode.type === 'Topic'
                      ? '#f3e5f5'
                      : selectedNode.type === 'Person'
                      ? '#fff3e0'
                      : '#e3f2fd',
                  color:
                    selectedNode.type === 'Topic'
                      ? '#9b59b6'
                      : selectedNode.type === 'Person'
                      ? '#e67e22'
                      : '#3498db',
                  fontSize: '14px',
                  fontWeight: '500',
                }}
              >
                {selectedNode.type}
              </span>
            </div>

            {selectedNode.description && (
              <div style={{ marginBottom: '16px' }}>
                <div style={{ fontSize: '12px', color: '#999', marginBottom: '4px' }}>Beschreibung</div>
                <div style={{ fontSize: '14px', lineHeight: '1.6', color: '#555' }}>{selectedNode.description}</div>
              </div>
            )}

            <button
              className="btn btn-secondary"
              onClick={() => setSelectedNode(null)}
              style={{ width: '100%', marginTop: '16px' }}
            >
              Schließen
            </button>
          </div>
        )}
      </div>

      {/* Legend */}
      <div className="card" style={{ marginTop: '20px', padding: '20px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Legende</h3>
        <div style={{ display: 'flex', gap: '30px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#3498db' }} />
            <span style={{ fontSize: '14px' }}>Konzept</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#9b59b6' }} />
            <span style={{ fontSize: '14px' }}>Thema</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#e67e22' }} />
            <span style={{ fontSize: '14px' }}>Person</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#2ecc71' }} />
            <span style={{ fontSize: '14px' }}>Ausgewählt</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphPage;
