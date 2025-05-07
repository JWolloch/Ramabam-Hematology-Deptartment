import React, { useState } from 'react';
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';

const stationData = {
  arrival: {
    name: 'Arrival',
    description: 'Where entities arrive into the system.',
    attributes: ['arrival_rate'],
    methods: ['generate_entity'],
  },
  queue_q_flow: {
    name: 'Queue to Q-Flow',
    description: 'Buffer before entering Q-Flow.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  q_flow: {
    name: 'Q-Flow',
    description: 'Handles service time distribution.',
    attributes: ['service_time_dist'],
    methods: ['process_entity'],
  },
  queue_secretary: {
    name: 'Queue to Secretary',
    description: 'Waiting area for secretary station.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  secretary_station: {
    name: 'Secretary Station',
    description: 'Secretary assists in registration and triage.',
    attributes: ['service_rate'],
    methods: ['process_registration'],
  },
  queue_nurse: {
    name: 'Queue to Nurse',
    description: 'Waiting line for available nurses.',
    attributes: ['queue_policy'],
    methods: ['assign_to_nurse'],
  },
  nurse_1: { name: 'Nurse 1', attributes: ['availability'], methods: ['treat_patient'] },
  nurse_2: { name: 'Nurse 2', attributes: ['availability'], methods: ['treat_patient'] },
  nurse_3: { name: 'Nurse 3', attributes: ['availability'], methods: ['treat_patient'] },
  nurse_4: { name: 'Nurse 4', attributes: ['availability'], methods: ['treat_patient'] },
  nurse_5: { name: 'Nurse 5', attributes: ['availability'], methods: ['treat_patient'] },
  blood_test_lab: { name: 'Blood Test Lab', attributes: ['test_capacity'], methods: ['analyze_sample'] },
  leukemia_doctor_1: { name: 'Leukemia Doctor 1', attributes: ['specialty'], methods: ['diagnose'] },
  leukemia_doctor_2: { name: 'Leukemia Doctor 2', attributes: ['specialty'], methods: ['diagnose'] },
  myeloma_doctor: { name: 'Myeloma Doctor', attributes: ['specialty'], methods: ['diagnose'] },
};

const nurseColor = '#42a5f5';
const myelomaColor = '#8e24aa';
const leukemiaColor = '#43a047';
const otherColor = '#e0e0e0';
const otherText = '#333';

const yellowGradient = 'linear-gradient(135deg, #fffde7 0%, #ffe082 100%)';
const orangeGradient = 'linear-gradient(135deg, #ffe0b2 0%, #ff9800 100%)';

const nodeStyle = {
  padding: 24,
  width: 200,
  height: 70,
  fontSize: 18,
  fontWeight: 600,
  textAlign: 'center',
  background: yellowGradient,
  color: otherText,
  border: '2px solid #bdbdbd',
  borderRadius: 20,
  boxShadow: '0 6px 16px rgba(186, 104, 200, 0.1)',
};

const bloodLabNodeStyle = {
  ...nodeStyle,
  background: orangeGradient,
  color: '#111',
  border: '2px solid #ef6c00',
};

const nurseNodeStyle = {
  ...nodeStyle,
  background: 'linear-gradient(135deg, #90caf9 0%, #42a5f5 100%)',
  color: '#fff',
  border: '2px solid #1565c0',
};
const myelomaNodeStyle = {
  ...nodeStyle,
  background: 'linear-gradient(135deg, #b39ddb 0%, #8e24aa 100%)',
  color: '#fff',
  border: '2px solid #6a1b9a',
};
const leukemiaNodeStyle = {
  ...nodeStyle,
  background: 'linear-gradient(135deg, #a5d6a7 0%, #43a047 100%)',
  color: '#fff',
  border: '2px solid #1b5e20',
};

const nurseY = [-300, -150, 0, 150, 300];

const nodes = [
  { id: 'arrival', data: { label: 'Arrival' }, position: { x: 0, y: 0 }, style: nodeStyle },
  { id: 'queue_q_flow', data: { label: 'Queue to Q-Flow' }, position: { x: 250, y: 0 }, style: nodeStyle },
  { id: 'q_flow', data: { label: 'Q-Flow' }, position: { x: 500, y: 0 }, style: nodeStyle },
  { id: 'queue_secretary', data: { label: 'Queue to Secretary' }, position: { x: 750, y: 0 }, style: nodeStyle },
  { id: 'secretary_station', data: { label: 'Secretary Station' }, position: { x: 1000, y: 0 }, style: nodeStyle },
  { id: 'queue_nurse', data: { label: 'Queue to Nurse' }, position: { x: 1250, y: 0 }, style: nodeStyle },
  ...[1, 2, 3, 4, 5].map((i, idx) => ({
    id: `nurse_${i}`,
    data: { label: `Nurse ${i}` },
    position: { x: 1500, y: nurseY[idx] },
    style: nurseNodeStyle,
  })),
  { id: 'blood_test_lab', data: { label: 'Blood Test Lab' }, position: { x: 1800, y: 0 }, style: bloodLabNodeStyle },
  { id: 'leukemia_doctor_1', data: { label: 'Leukemia Doctor 1' }, position: { x: 2050, y: -200 }, style: leukemiaNodeStyle },
  { id: 'leukemia_doctor_2', data: { label: 'Leukemia Doctor 2' }, position: { x: 2050, y: -80 }, style: leukemiaNodeStyle },
  { id: 'myeloma_doctor', data: { label: 'Myeloma Doctor' }, position: { x: 2050, y: 150 }, style: myelomaNodeStyle },
  {
    id: 'legend',
    position: { x: 800, y: -300 },
    data: {
      label: (
        <div style={{ fontSize: 16, padding: '10px' }}>
          <strong style={{ fontSize: 20, marginBottom: '10px', display: 'block', borderBottom: '2px solid #ccc', paddingBottom: '5px' }}>Flow Paths Legend</strong>
          <div style={{ marginBottom: '8px' }}>
            <span style={{ color: '#6a1b9a', fontWeight: 'bold' }}>●</span> Myeloma Direct Path
            <div style={{ fontSize: 14, color: '#666', marginLeft: '20px' }}>Nurse → Myeloma Doctor</div>
          </div>
          <div style={{ marginBottom: '8px' }}>
            <span style={{ color: '#ec407a', fontWeight: 'bold' }}>●</span> Myeloma Lab Path
            <div style={{ fontSize: 14, color: '#666', marginLeft: '20px' }}>Nurse → Blood Lab → Myeloma Doctor</div>
          </div>
          <div style={{ marginBottom: '8px' }}>
            <span style={{ color: '#43a047', fontWeight: 'bold' }}>●</span> Leukemia Path
            <div style={{ fontSize: 14, color: '#666', marginLeft: '20px' }}>Nurse → Blood Lab → Leukemia Doctor</div>
          </div>
        </div>
      ),
    },
    style: {
      padding: 15,
      width: 280,
      border: '2px solid #e0e0e0',
      background: '#ffffff',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      fontSize: 15,
    },
    draggable: false,
  },
];

const edges = [
  { id: 'arrival-queue_q_flow', source: 'arrival', target: 'queue_q_flow', style: { stroke: '#f8bbd0', strokeWidth: 4 } },
  { id: 'queue_q_flow-q_flow', source: 'queue_q_flow', target: 'q_flow', style: { stroke: '#f8bbd0', strokeWidth: 4 } },
  { id: 'q_flow-queue_secretary', source: 'q_flow', target: 'queue_secretary', style: { stroke: '#f8bbd0', strokeWidth: 4 } },
  { id: 'queue_secretary-secretary_station', source: 'queue_secretary', target: 'secretary_station', style: { stroke: '#f8bbd0', strokeWidth: 4 } },
  { id: 'secretary_station-queue_nurse', source: 'secretary_station', target: 'queue_nurse', style: { stroke: '#f8bbd0', strokeWidth: 4 } },
  ...[1, 2, 3, 4, 5].map(i => ({
    id: `queue_nurse-nurse_${i}`,
    source: 'queue_nurse',
    target: `nurse_${i}`,
    style: { stroke: '#f8bbd0', strokeWidth: 4 },
  })),
  ...[1, 2, 3, 4, 5].map(i => ({
    id: `myeloma1-nurse_${i}`,
    source: `nurse_${i}`,
    target: 'myeloma_doctor',
    style: { stroke: '#6a1b9a', strokeWidth: 4 },
  })),
  ...[1, 2, 3, 4, 5].map(i => ({
    id: `myeloma2-nurse_${i}`,
    source: `nurse_${i}`,
    target: 'blood_test_lab',
    style: { stroke: '#ec407a', strokeWidth: 4 },
  })),
  {
    id: 'bloodlab-myeloma',
    source: 'blood_test_lab',
    target: 'myeloma_doctor',
    style: { stroke: '#ec407a', strokeWidth: 4 },
  },
  ...[1, 2, 3, 4, 5].map(i => ({
    id: `leukemia-nurse_${i}`,
    source: `nurse_${i}`,
    target: 'blood_test_lab',
    style: { stroke: '#42a5f5', strokeDasharray: '4 2', strokeWidth: 4 },
  })),
  {
    id: 'bloodlab-leukemia-1',
    source: 'blood_test_lab',
    target: 'leukemia_doctor_1',
    style: { stroke: '#42a5f5', strokeWidth: 4 },
  },
  {
    id: 'bloodlab-leukemia-2',
    source: 'blood_test_lab',
    target: 'leukemia_doctor_2',
    style: { stroke: '#42a5f5', strokeWidth: 4 },
  },
];

export default function App() {
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <div style={{ height: '100vh', width: '100%', display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodeClick={(event, node) => setSelectedNode(stationData[node.id])}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      {selectedNode && (
        <div style={{ width: 300, padding: 20, background: '#eee', overflowY: 'auto', position: 'relative' }}>
          <button
            onClick={() => setSelectedNode(null)}
            style={{
              position: 'absolute',
              top: 10,
              right: 10,
              background: 'red',
              color: 'white',
              border: 'none',
              borderRadius: '50%',
              width: '30px',
              height: '30px',
              cursor: 'pointer',
            }}
          >
            ×
          </button>
          <h2>{selectedNode.name}</h2>
          <p>{selectedNode.description}</p>
          <h4>Attributes</h4>
          <ul>{selectedNode.attributes.map(attr => <li key={attr}>{attr}</li>)}</ul>
          <h4>Methods</h4>
          <ul>{selectedNode.methods.map(method => <li key={method}>{method}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
