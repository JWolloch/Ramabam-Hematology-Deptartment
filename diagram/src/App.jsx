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
    name: 'Queue to Nurses',
    description: 'Waiting line for available nurses.',
    attributes: ['queue_policy'],
    methods: ['assign_to_nurse'],
  },
  queue_nurse_1: {
    name: 'Queue to Nurse 1',
    description: 'Dedicated waiting line for Nurse 1.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_nurse_2: {
    name: 'Queue to Nurse 2',
    description: 'Dedicated waiting line for Nurse 2.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_nurse_3: {
    name: 'Queue to Nurse 3',
    description: 'Dedicated waiting line for Nurse 3.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_nurse_4: {
    name: 'Queue to Nurse 4',
    description: 'Dedicated waiting line for Nurse 4.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_nurse_5: {
    name: 'Queue to Nurse 5',
    description: 'Dedicated waiting line for Nurse 5.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  nurse_1: { name: 'Nurse 1', attributes: ['mean_service_duration_regular_treatment', 'mean_service_treatment_complex_treatment'], methods: ['treat_patient'] },
  nurse_2: { name: 'Nurse 2', attributes: ['mean_service_duration_regular_treatment', 'mean_service_treatment_complex_treatment'], methods: ['treat_patient'] },
  nurse_3: { name: 'Nurse 3', attributes: ['mean_service_duration_regular_treatment', 'mean_service_treatment_complex_treatment'], methods: ['treat_patient'] },
  nurse_4: { name: 'Nurse 4', attributes: ['mean_service_duration_regular_treatment', 'mean_service_treatment_complex_treatment'], methods: ['treat_patient'] },
  nurse_5: { name: 'Nurse 5', attributes: ['mean_service_duration_regular_treatment', 'mean_service_treatment_complex_treatment'], methods: ['treat_patient'] },
  blood_test_lab: { name: 'Blood Test Lab', attributes: [''], methods: ['analyze_sample'] },
  leukemia_doctor_1: { name: 'Leukemia Doctor 1', attributes: ['specialty'], methods: ['diagnose'] },
  leukemia_doctor_2: { name: 'Leukemia Doctor 2', attributes: ['specialty'], methods: ['diagnose'] },
  transplant_doctor: { name: 'Transplant Doctor', attributes: ['specialty'], methods: ['diagnose'] },
  queue_leukemia_doctor_1: {
    name: 'Queue to Leukemia Doctor 1',
    description: 'Waiting area for Leukemia Doctor 1.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_leukemia_doctor_2: {
    name: 'Queue to Leukemia Doctor 2',
    description: 'Waiting area for Leukemia Doctor 2.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
  queue_transplant_doctor: {
    name: 'Queue to Transplant Doctor',
    description: 'Waiting area for Transplant Doctor.',
    attributes: ['queue_length'],
    methods: ['enqueue', 'dequeue'],
  },
};

const COLORS = {
  arrival: '#FD3DB5',          // Hot Pink
  qflow: '#FFB8DC',            // Baby Pink
  secretary: '#FB6A2C',        // Tangerine Orange
  nurse: '#8C1946',            // Deep Berry
  lab: '#D1A1D7',              // Soft Lilac
  leukemia: '#660066',         // Plum Purple
  transplant: '#FFE156',          // Lemon Zest
};

const GRADIENTS = {
  arrival: 'linear-gradient(135deg, #FD3DB5 0%, #ff69b4 100%)',
  qflow: 'linear-gradient(135deg, #FFB8DC 0%, #fd3db5 100%)',
  secretary: 'linear-gradient(135deg, #FB6A2C 0%, #ff9800 100%)',
  nurse: 'linear-gradient(135deg, #8C1946 0%, #c2185b 100%)',
  lab: 'linear-gradient(135deg, #D1A1D7 0%, #a084af 100%)',
  leukemia: 'linear-gradient(135deg, #660066 0%, #a020f0 100%)',
  transplant: 'linear-gradient(135deg, #FFE156 0%, #ffd600 100%)',
};

const nodeStyle = {
  padding: 24,
  width: 200,
  height: 70,
  fontSize: 18,
  fontWeight: 600,
  textAlign: 'center',
  background: GRADIENTS.qflow,
  color: '#222',
  border: '2px solid #bdbdbd',
  borderRadius: 20,
  boxShadow: '0 6px 16px rgba(186, 104, 200, 0.1)',
};

const arrivalNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.arrival,
  color: '#fff',
  border: `2px solid ${COLORS.arrival}`,
};
const secretaryNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.secretary,
  color: '#fff',
  border: `2px solid ${COLORS.secretary}`,
};
const nurseNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.nurse,
  color: '#fff',
  border: `2px solid ${COLORS.nurse}`,
};
const bloodLabNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.lab,
  color: '#222',
  border: `2px solid ${COLORS.lab}`,
};
const leukemiaNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.leukemia,
  color: '#fff',
  border: `2px solid ${COLORS.leukemia}`,
};
const transplantNodeStyle = {
  ...nodeStyle,
  background: GRADIENTS.transplant,
  color: '#222',
  border: `2px solid ${COLORS.transplant}`,
};

const QflowQueueNodeStyle = {
  ...nodeStyle,
  width: 120,
  height: 90,
  background: 'linear-gradient(135deg, #FFB8DC 0%, #fd3db5 100%)',
  border: `2px dashed ${COLORS.qflow}`,
  color: '#333',
  fontStyle: 'italic',
  opacity: 0.75,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const SecretaryQueueNodeStyle = {
  ...nodeStyle,
  width: 120,
  height: 90,
  background: 'linear-gradient(135deg, #FB6A2C 0%, #ff9800 100%)',
  border: `2px dashed ${COLORS.secretary}`,
  color: '#333',
  fontStyle: 'italic',
  opacity: 0.75,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const NurseQueueNodeStyle = {
  ...nodeStyle,
  width: 120,
  height: 90,
  background: 'linear-gradient(135deg, #8C1946 0%, #c2185b 100%)',
  border: `2px dashed ${COLORS.nurse}`,
  color: '#fff',
  fontStyle: 'italic',
  opacity: 0.75,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};


const LeukemiaDoctorQueueNodeStyle = {
  ...nodeStyle,
  width: 120,
  height: 90,
  background: 'linear-gradient(135deg, #660066 0%, #a020f0 100%)',
  border: `2px dashed ${COLORS.leukemia}`,
  color: '#fff',
  fontStyle: 'italic',
  opacity: 0.75,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const TransplantDoctorQueueNodeStyle = {
  ...nodeStyle,
  width: 120,
  height: 90,
  background: 'linear-gradient(135deg, #FFE156 0%, #ffd600 100%)',
  border: `2px dashed ${COLORS.transplant}`,
  color: '#333',
  fontStyle: 'italic',
  opacity: 0.75,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const nurseY = [-300, -150, 0, 150, 300];

const nodes = [
  { id: 'arrival', data: { label: 'Arrival' }, position: { x: 0, y: 0 }, style: arrivalNodeStyle },
  { id: 'queue_q_flow', type: 'queue', data: { label: 'Queue to Q-Flow' }, position: { x: 275, y: -7.5 }, style: QflowQueueNodeStyle },
  { id: 'q_flow', data: { label: 'Q-Flow' }, position: { x: 500, y: 0 }, style: nodeStyle },
  { id: 'queue_secretary', type: 'queue', data: { label: 'Queue to Secretary' }, position: { x: 775, y: -7.5 }, style: SecretaryQueueNodeStyle },
  { id: 'secretary_station', data: { label: 'Secretary Station' }, position: { x: 1000, y: 0 }, style: secretaryNodeStyle },
  { id: 'queue_nurse', type: 'queue', data: { label: 'Queue to Nurses' }, position: { x: 1275, y: -7.5 }, style: NurseQueueNodeStyle },
  ...[1, 2, 3, 4, 5].map((i, idx) => ({
    id: `nurse_${i}`,
    data: { label: `Nurse ${i}` },
    position: { x: 1500, y: nurseY[idx] },
    style: nurseNodeStyle,
  })),
  { id: 'blood_test_lab', data: { label: 'Blood Test Lab' }, position: { x: 1800, y: 0 }, style: bloodLabNodeStyle },
  { id: 'queue_leukemia_doctor_1', type: 'queue', data: { label: 'Queue to Leukemia Doctor 1' }, position: { x: 2025, y: -207.5 }, style: LeukemiaDoctorQueueNodeStyle },
  { id: 'queue_leukemia_doctor_2', type: 'queue', data: { label: 'Queue to Leukemia Doctor 2' }, position: { x: 2025, y: -87.5 }, style: LeukemiaDoctorQueueNodeStyle },
  { id: 'queue_transplant_doctor', type: 'queue', data: { label: 'Queue to Transplant Doctor' }, position: { x: 2025, y: 142.5 }, style: TransplantDoctorQueueNodeStyle },
  { id: 'leukemia_doctor_1', data: { label: 'Leukemia Doctor 1' }, position: { x: 2200, y: -200 }, style: leukemiaNodeStyle },
  { id: 'leukemia_doctor_2', data: { label: 'Leukemia Doctor 2' }, position: { x: 2200, y: -80 }, style: leukemiaNodeStyle },
  { id: 'transplant_doctor', data: { label: 'Transplant Doctor' }, position: { x: 2200, y: 150 }, style: transplantNodeStyle },
  {
    id: 'legend',
    position: { x: 400, y: -350 },
    data: {
      label: (
        <div style={{ fontSize: 18, padding: '15px' }}>
          <strong style={{ fontSize: 24, marginBottom: '15px', display: 'block', borderBottom: '2px solid #ccc', paddingBottom: '8px' }}>Flow Paths Legend</strong>
          <div style={{ marginBottom: '12px' }}>
            <span style={{ color: '#6a1b9a', fontWeight: 'bold', fontSize: 20 }}>●</span> <span style={{ fontWeight: 'bold' }}>Transplant Direct Path</span>
            <div style={{ fontSize: 16, color: '#333', marginLeft: '25px', marginTop: '5px' }}>Nurse → Transplant Doctor</div>
          </div>
          <div style={{ marginBottom: '12px' }}>
            <span style={{ color: '#ec407a', fontWeight: 'bold', fontSize: 20 }}>●</span> <span style={{ fontWeight: 'bold' }}>Transplant Lab Path</span>
            <div style={{ fontSize: 16, color: '#333', marginLeft: '25px', marginTop: '5px' }}>Nurse → Blood Lab → Transplant Doctor</div>
          </div>
          <div style={{ marginBottom: '12px' }}>
            <span style={{ color: '#42a5f5', fontWeight: 'bold', fontSize: 20 }}>●</span> <span style={{ fontWeight: 'bold' }}>Leukemia Path</span>
            <div style={{ fontSize: 16, color: '#333', marginLeft: '25px', marginTop: '5px' }}>Nurse → Blood Lab → Leukemia Doctor</div>
          </div>
        </div>
      ),
    },
    style: {
      padding: 20,
      width: 360,
      border: '2px solid #e0e0e0',
      background: '#ffffff',
      borderRadius: '12px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
      fontSize: 16,
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
    id: `transplant1-nurse_${i}`,
    source: `nurse_${i}`,
    target: 'transplant_doctor',
    style: { stroke: '#6a1b9a', strokeWidth: 4 },
  })),
  ...[1, 2, 3, 4, 5].map(i => ({
    id: `transplant2-nurse_${i}`,
    source: `nurse_${i}`,
    target: 'blood_test_lab',
    style: { stroke: '#ec407a', strokeWidth: 4 },
  })),
  { id: 'bloodlab-queue_transplant', source: 'blood_test_lab', target: 'queue_transplant_doctor', style: { stroke: '#ec407a', strokeWidth: 4 } },
  { id: 'bloodlab-queue_leukemia_1', source: 'blood_test_lab', target: 'queue_leukemia_doctor_1', style: { stroke: '#42a5f5', strokeWidth: 4 } },
  { id: 'bloodlab-queue_leukemia_2', source: 'blood_test_lab', target: 'queue_leukemia_doctor_2', style: { stroke: '#42a5f5', strokeWidth: 4 } },
  { id: 'queue_transplant_doctor-transplant_doctor', source: 'queue_transplant_doctor', target: 'transplant_doctor', style: { stroke: '#ec407a', strokeWidth: 4 } },
  { id: 'queue_leukemia_doctor_1-leukemia_doctor_1', source: 'queue_leukemia_doctor_1', target: 'leukemia_doctor_1', style: { stroke: '#42a5f5', strokeWidth: 4 } },
  { id: 'queue_leukemia_doctor_2-leukemia_doctor_2', source: 'queue_leukemia_doctor_2', target: 'leukemia_doctor_2', style: { stroke: '#42a5f5', strokeWidth: 4 } },
];

export default function App() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [useIndividualQueues, setUseIndividualQueues] = useState(false);

  // Create individual queue nodes for nurses when toggle is active
  const individualNurseQueues = useIndividualQueues ? [1, 2, 3, 4, 5].map((i, idx) => ({
    id: `queue_nurse_${i}`,
    type: 'queue',
    data: { label: `Queue to Nurse ${i}` },
    position: { x: 1275, y: nurseY[idx] },
    style: NurseQueueNodeStyle,
  })) : [];

  // Individual queue to nurse edges
  const individualQueueEdges = useIndividualQueues ? [
    ...([1, 2, 3, 4, 5].map(i => ({
      id: `secretary_station-queue_nurse_${i}`,
      source: 'secretary_station',
      target: `queue_nurse_${i}`,
      style: { stroke: '#f8bbd0', strokeWidth: 4 },
    }))),
    ...([1, 2, 3, 4, 5].map(i => ({
      id: `queue_nurse_${i}-nurse_${i}`,
      source: `queue_nurse_${i}`,
      target: `nurse_${i}`,
      style: { stroke: '#f8bbd0', strokeWidth: 4 },
    })))
  ] : [];

  // Filter out the common queue and its connections when using individual queues
  const filteredNodes = [...nodes.filter(node => 
    !(useIndividualQueues && node.id === 'queue_nurse')
  ), ...individualNurseQueues];

  const filteredEdges = [...edges.filter(edge => 
    !(useIndividualQueues && 
      (edge.id === 'secretary_station-queue_nurse' || 
       edge.id.startsWith('queue_nurse-nurse_')))
  ), ...individualQueueEdges];

  return (
    <div style={{ height: '100vh', width: '100%', display: 'flex' }}>
      <div style={{ flex: 1, position: 'relative' }}>
        <div style={{ 
          position: 'absolute', 
          top: 10, 
          right: 10, 
          zIndex: 10, 
          background: 'white',
          padding: '8px 12px',
          borderRadius: 8,
          boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <button 
            onClick={() => setUseIndividualQueues(!useIndividualQueues)}
            style={{
              background: useIndividualQueues ? COLORS.nurse : '#f8bbd0',
              padding: '8px 16px',
              border: 'none',
              borderRadius: 20,
              color: useIndividualQueues ? 'white' : '#222',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              minWidth: '180px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}
          >
            {useIndividualQueues ? 'Individual Queues' : 'Single Queue'}
          </button>
        </div>
        
        <div style={{
          position: 'absolute',
          top: 60,
          right: 10,
          zIndex: 10,
          background: 'white',
          padding: '12px',
          borderRadius: 8,
          boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
          width: '300px',
          fontSize: '14px',
          lineHeight: 1.4
        }}>
          <strong>Queue Policies:</strong><br/>
          <strong>Single Queue:</strong> One queue serving all nurses<br/>
          <strong>Individual Queues:</strong> Each nurse has a dedicated queue
        </div>
        
        <ReactFlow
          nodes={filteredNodes}
          edges={filteredEdges}
          onNodeClick={(event, node) => setSelectedNode(node)}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>

      {selectedNode && (
        <div style={{ 
          width: 300, 
          padding: 20, 
          background: selectedNode.id === 'queue_q_flow' ? QflowQueueNodeStyle.background :
                     selectedNode.id === 'queue_secretary' ? SecretaryQueueNodeStyle.background :
                     selectedNode.id === 'queue_nurse' ? NurseQueueNodeStyle.background :
                     selectedNode.id.startsWith('queue_nurse_') ? NurseQueueNodeStyle.background :
                     selectedNode.id === 'queue_leukemia_doctor_1' ? LeukemiaDoctorQueueNodeStyle.background :
                     selectedNode.id === 'queue_leukemia_doctor_2' ? LeukemiaDoctorQueueNodeStyle.background :
                     selectedNode.id === 'queue_transplant_doctor' ? TransplantDoctorQueueNodeStyle.background :
                     selectedNode.id?.includes('nurse') ? nurseNodeStyle.background :
                     selectedNode.id?.includes('transplant') ? transplantNodeStyle.background :
                     selectedNode.id?.includes('leukemia') ? leukemiaNodeStyle.background :
                     selectedNode.id?.includes('blood_test') ? bloodLabNodeStyle.background :
                     selectedNode.id === 'arrival' ? arrivalNodeStyle.background :
                     selectedNode.id === 'q_flow' ? nodeStyle.background :
                     selectedNode.id === 'secretary_station' ? secretaryNodeStyle.background :
                     nodeStyle.background,
          color: selectedNode.id === 'queue_q_flow' ? QflowQueueNodeStyle.color :
                 selectedNode.id === 'queue_secretary' ? SecretaryQueueNodeStyle.color :
                 selectedNode.id === 'queue_nurse' ? NurseQueueNodeStyle.color :
                 selectedNode.id.startsWith('queue_nurse_') ? NurseQueueNodeStyle.color :
                 selectedNode.id === 'queue_leukemia_doctor_1' ? LeukemiaDoctorQueueNodeStyle.color :
                 selectedNode.id === 'queue_leukemia_doctor_2' ? LeukemiaDoctorQueueNodeStyle.color :
                 selectedNode.id === 'queue_transplant_doctor' ? TransplantDoctorQueueNodeStyle.color :
                 selectedNode.id?.includes('nurse') || 
                 selectedNode.id?.includes('leukemia') || 
                 selectedNode.id === 'arrival' || 
                 selectedNode.id === 'secretary_station' ? '#fff' : '#222',
          overflowY: 'auto', 
          position: 'relative',
          boxShadow: '0 0 20px rgba(0,0,0,0.1)',
          borderLeft: '1px solid rgba(0,0,0,0.1)'
        }}>
          <button
            onClick={() => setSelectedNode(null)}
            style={{
              position: 'absolute',
              top: 10,
              right: 10,
              background: 'rgba(255,255,255,0.2)',
              color: selectedNode.id?.includes('nurse') || 
                     selectedNode.id?.includes('leukemia') || 
                     selectedNode.id === 'arrival' || 
                     selectedNode.id === 'secretary_station' ? '#fff' : '#222',
              border: 'none',
              borderRadius: '50%',
              width: '30px',
              height: '30px',
              cursor: 'pointer',
              fontSize: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease',
              ':hover': {
                background: 'rgba(255,255,255,0.3)'
              }
            }}
          >
            ×
          </button>
          <h2 style={{ 
            marginTop: 0,
            fontSize: '24px',
            borderBottom: '2px solid rgba(255,255,255,0.2)',
            paddingBottom: '10px'
          }}>{stationData[selectedNode.id]?.name || selectedNode.data?.label}</h2>
          <p style={{ 
            fontSize: '16px',
            lineHeight: '1.5',
            opacity: 0.9
          }}>{stationData[selectedNode.id]?.description || ''}</p>
          <h4 style={{ 
            marginTop: '20px',
            fontSize: '18px',
            borderBottom: '1px solid rgba(255,255,255,0.2)',
            paddingBottom: '5px'
          }}>Attributes</h4>
          <ul style={{ 
            listStyle: 'none',
            padding: 0,
            margin: '10px 0'
          }}>
            {(stationData[selectedNode.id]?.attributes || []).map(attr => (
              <li key={attr} style={{
                padding: '8px 12px',
                margin: '5px 0',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '6px',
                fontSize: '14px'
              }}>{attr}</li>
            ))}
          </ul>
          <h4 style={{ 
            marginTop: '20px',
            fontSize: '18px',
            borderBottom: '1px solid rgba(255,255,255,0.2)',
            paddingBottom: '5px'
          }}>Methods</h4>
          <ul style={{ 
            listStyle: 'none',
            padding: 0,
            margin: '10px 0'
          }}>
            {(stationData[selectedNode.id]?.methods || []).map(method => (
              <li key={method} style={{
                padding: '8px 12px',
                margin: '5px 0',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '6px',
                fontSize: '14px'
              }}>{method}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}