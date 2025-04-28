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

const nodes = [
  { id: 'arrival', data: { label: 'Arrival' }, position: { x: 0, y: 0 } },
  { id: 'queue_q_flow', data: { label: 'Queue to Q-Flow' }, position: { x: 200, y: 0 } },
  { id: 'q_flow', data: { label: 'Q-Flow' }, position: { x: 400, y: 0 } },
  { id: 'queue_secretary', data: { label: 'Queue to Secretary' }, position: { x: 600, y: 0 } },
  { id: 'secretary_station', data: { label: 'Secretary Station' }, position: { x: 800, y: 0 } },
  { id: 'queue_nurse', data: { label: 'Queue to Nurse' }, position: { x: 1000, y: 0 } },
  { id: 'nurse_1', data: { label: 'Nurse 1' }, position: { x: 1200, y: -200 } },
  { id: 'nurse_2', data: { label: 'Nurse 2' }, position: { x: 1200, y: -100 } },
  { id: 'nurse_3', data: { label: 'Nurse 3' }, position: { x: 1200, y: 0 } },
  { id: 'nurse_4', data: { label: 'Nurse 4' }, position: { x: 1200, y: 100 } },
  { id: 'nurse_5', data: { label: 'Nurse 5' }, position: { x: 1200, y: 200 } },
  { id: 'blood_test_lab', data: { label: 'Blood Test Lab' }, position: { x: 1500, y: 0 } },
  { id: 'leukemia_doctor_1', data: { label: 'Leukemia Doctor 1' }, position: { x: 1800, y: -100 } },
  { id: 'leukemia_doctor_2', data: { label: 'Leukemia Doctor 2' }, position: { x: 1800, y: 0 } },
  { id: 'myeloma_doctor', data: { label: 'Myeloma Doctor' }, position: { x: 1800, y: 100 } },
];

const edges = [
  { id: 'arrival-queue_q_flow', source: 'arrival', target: 'queue_q_flow' },
  { id: 'queue_q_flow-q_flow', source: 'queue_q_flow', target: 'q_flow' },
  { id: 'q_flow-queue_secretary', source: 'q_flow', target: 'queue_secretary' },
  { id: 'queue_secretary-secretary_station', source: 'queue_secretary', target: 'secretary_station' },
  { id: 'secretary_station-queue_nurse', source: 'secretary_station', target: 'queue_nurse' },
  { id: 'queue_nurse-nurse_1', source: 'queue_nurse', target: 'nurse_1' },
  { id: 'queue_nurse-nurse_2', source: 'queue_nurse', target: 'nurse_2' },
  { id: 'queue_nurse-nurse_3', source: 'queue_nurse', target: 'nurse_3' },
  { id: 'queue_nurse-nurse_4', source: 'queue_nurse', target: 'nurse_4' },
  { id: 'queue_nurse-nurse_5', source: 'queue_nurse', target: 'nurse_5' },
  { id: 'nurse_1-blood_test_lab', source: 'nurse_1', target: 'blood_test_lab' },
  { id: 'nurse_2-blood_test_lab', source: 'nurse_2', target: 'blood_test_lab' },
  { id: 'nurse_3-blood_test_lab', source: 'nurse_3', target: 'blood_test_lab' },
  { id: 'nurse_4-blood_test_lab', source: 'nurse_4', target: 'blood_test_lab' },
  { id: 'nurse_5-blood_test_lab', source: 'nurse_5', target: 'blood_test_lab' },
  { id: 'nurse_1-myeloma_doctor', source: 'nurse_1', target: 'myeloma_doctor' },
  { id: 'nurse_2-myeloma_doctor', source: 'nurse_2', target: 'myeloma_doctor' },
  { id: 'nurse_3-myeloma_doctor', source: 'nurse_3', target: 'myeloma_doctor' },
  { id: 'nurse_4-myeloma_doctor', source: 'nurse_4', target: 'myeloma_doctor' },
  { id: 'nurse_5-myeloma_doctor', source: 'nurse_5', target: 'myeloma_doctor' },
  { id: 'blood_test_lab-leukemia_doctor_1', source: 'blood_test_lab', target: 'leukemia_doctor_1' },
  { id: 'blood_test_lab-leukemia_doctor_2', source: 'blood_test_lab', target: 'leukemia_doctor_2' },
  { id: 'blood_test_lab-myeloma_doctor', source: 'blood_test_lab', target: 'myeloma_doctor' },
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
