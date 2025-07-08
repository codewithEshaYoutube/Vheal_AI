import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import json
from typing import Dict, List, Any
import uuid

# Page configuration
st.set_page_config(
    page_title="VHeal AI - Agentic Hospital Discharge Copilot",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .patient-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    
    .alert-card {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .success-card {
        background: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    
    .agent-status {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .agent-active {
        background: #28a745;
        color: white;
    }
    
    .agent-processing {
        background: #ffc107;
        color: black;
    }
    
    .agent-completed {
        background: #6c757d;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'patients' not in st.session_state:
    st.session_state.patients = []
if 'discharge_history' not in st.session_state:
    st.session_state.discharge_history = []
if 'ai_agents' not in st.session_state:
    st.session_state.ai_agents = []
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# Sample data initialization
def initialize_sample_data():
    if not st.session_state.patients:
        st.session_state.patients = [
            {
                "id": "PT001",
                "name": "John Smith",
                "age": 68,
                "condition": "Post-surgical recovery",
                "room": "302A",
                "discharge_status": "Ready for Discharge",
                "doctor": "Dr. Sarah Johnson",
                "admission_date": "2024-12-15",
                "estimated_discharge": "2024-12-18",
                "checklist_completion": 85,
                "priority": "High",
                "tasks": {
                    "vitals_check": True,
                    "lab_results": True,
                    "medication_review": True,
                    "discharge_summary": False,
                    "insurance_approval": True,
                    "transport_arranged": False
                }
            },
            {
                "id": "PT002",
                "name": "Maria Garcia",
                "age": 45,
                "condition": "Pneumonia treatment",
                "room": "215B",
                "discharge_status": "Pending Medical Review",
                "doctor": "Dr. Michael Chen",
                "admission_date": "2024-12-16",
                "estimated_discharge": "2024-12-19",
                "checklist_completion": 60,
                "priority": "Medium",
                "tasks": {
                    "vitals_check": True,
                    "lab_results": False,
                    "medication_review": True,
                    "discharge_summary": False,
                    "insurance_approval": True,
                    "transport_arranged": False
                }
            },
            {
                "id": "PT003",
                "name": "Robert Wilson",
                "age": 72,
                "condition": "Cardiac monitoring",
                "room": "401C",
                "discharge_status": "Awaiting Pharmacy",
                "doctor": "Dr. Lisa Park",
                "admission_date": "2024-12-14",
                "estimated_discharge": "2024-12-18",
                "checklist_completion": 90,
                "priority": "High",
                "tasks": {
                    "vitals_check": True,
                    "lab_results": True,
                    "medication_review": False,
                    "discharge_summary": True,
                    "insurance_approval": True,
                    "transport_arranged": True
                }
            }
        ]

# AI Agent simulation
class AIAgent:
    def __init__(self, name, role, status="active"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.status = status
        self.current_task = None
        self.tasks_completed = 0
        self.created_at = datetime.now()
    
    def assign_task(self, task, patient_id):
        self.current_task = {
            "task": task,
            "patient_id": patient_id,
            "started_at": datetime.now()
        }
        self.status = "processing"
    
    def complete_task(self):
        self.tasks_completed += 1
        self.current_task = None
        self.status = "active"

def create_ai_agents():
    agents = [
        AIAgent("Summary Agent", "Discharge Summary Generation"),
        AIAgent("Coordination Agent", "Staff Coordination"),
        AIAgent("Checklist Agent", "Task Completion Monitoring"),
        AIAgent("Alert Agent", "Notification Management")
    ]
    return agents

# Main application
def main():
    # Initialize data
    initialize_sample_data()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚑 VHeal AI - Agentic Hospital Discharge Copilot</h1>
        <p>Autonomous AI-powered discharge coordination for modern hospitals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🤖 AI Agent Control Panel")
        
        # Agent status
        if st.button("🚀 Initialize AI Agents"):
            st.session_state.ai_agents = create_ai_agents()
            st.success("AI Agents initialized!")
        
        if st.session_state.ai_agents:
            st.subheader("Active Agents")
            for agent in st.session_state.ai_agents:
                status_class = f"agent-{agent.status}"
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <strong>{agent.name}</strong><br>
                    <span class="agent-status {status_class}">{agent.status.upper()}</span><br>
                    <small>{agent.role}</small><br>
                    <small>Tasks completed: {agent.tasks_completed}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Quick actions
        st.subheader("Quick Actions")
        if st.button("📝 Generate Discharge Summary"):
            simulate_ai_action("discharge_summary")
        
        if st.button("📞 Coordinate Staff"):
            simulate_ai_action("staff_coordination")
        
        if st.button("🔔 Send Notifications"):
            simulate_ai_action("notifications")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Patients", len(st.session_state.patients))
    
    with col2:
        ready_count = sum(1 for p in st.session_state.patients if p['discharge_status'] == 'Ready for Discharge')
        st.metric("Ready for Discharge", ready_count)
    
    with col3:
        avg_completion = sum(p['checklist_completion'] for p in st.session_state.patients) / len(st.session_state.patients) if st.session_state.patients else 0
        st.metric("Avg Checklist Completion", f"{avg_completion:.1f}%")
    
    with col4:
        active_agents = len([a for a in st.session_state.ai_agents if a.status == "active"])
        st.metric("Active AI Agents", active_agents)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Patient Dashboard", "🤖 AI Agent Activity", "📊 Analytics", "🔔 Notifications"])
    
    with tab1:
        st.subheader("Patient Discharge Status")
        
        # Patient cards
        for patient in st.session_state.patients:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="patient-card">
                        <h4>{patient['name']} ({patient['id']})</h4>
                        <p><strong>Age:</strong> {patient['age']} | <strong>Room:</strong> {patient['room']}</p>
                        <p><strong>Condition:</strong> {patient['condition']}</p>
                        <p><strong>Doctor:</strong> {patient['doctor']}</p>
                        <p><strong>Status:</strong> {patient['discharge_status']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Checklist completion
                    progress = patient['checklist_completion'] / 100
                    st.progress(progress, text=f"Checklist: {patient['checklist_completion']}%")
                    
                    # Task breakdown
                    completed_tasks = sum(1 for task, status in patient['tasks'].items() if status)
                    total_tasks = len(patient['tasks'])
                    st.write(f"Tasks: {completed_tasks}/{total_tasks}")
                
                with col3:
                    # Priority badge
                    priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    st.write(f"Priority: {priority_color.get(patient['priority'], '⚪')} {patient['priority']}")
                    
                    # Action buttons
                    if st.button(f"🤖 AI Assist", key=f"assist_{patient['id']}"):
                        simulate_ai_assistance(patient['id'])
                    
                    if st.button(f"📄 View Details", key=f"details_{patient['id']}"):
                        show_patient_details(patient)
    
    with tab2:
        st.subheader("AI Agent Activity Log")
        
        # Real-time agent activity simulation
        if st.session_state.ai_agents:
            for agent in st.session_state.ai_agents:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="agent-card">
                            <h4>🤖 {agent.name}</h4>
                            <p><strong>Role:</strong> {agent.role}</p>
                            <p><strong>Status:</strong> {agent.status}</p>
                            {f"<p><strong>Current Task:</strong> {agent.current_task['task']} for {agent.current_task['patient_id']}</p>" if agent.current_task else ""}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if agent.status == "processing":
                            st.spinner("Processing...")
                        elif agent.status == "active":
                            st.success("Ready")
                        else:
                            st.info("Idle")
        
        # Activity timeline
        st.subheader("Recent AI Actions")
        activities = [
            {"time": "2024-12-18 14:30", "agent": "Summary Agent", "action": "Generated discharge summary for PT001", "status": "completed"},
            {"time": "2024-12-18 14:25", "agent": "Coordination Agent", "action": "Coordinated pharmacy pickup for PT003", "status": "completed"},
            {"time": "2024-12-18 14:20", "agent": "Alert Agent", "action": "Sent notification to transport team", "status": "completed"},
            {"time": "2024-12-18 14:15", "agent": "Checklist Agent", "action": "Updated task completion for PT002", "status": "completed"},
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="success-card">
                <p><strong>{activity['time']}</strong> - {activity['agent']}</p>
                <p>{activity['action']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Hospital Discharge Analytics")
        
        # Create sample analytics data
        discharge_data = pd.DataFrame({
            'Date': pd.date_range('2024-12-01', periods=18, freq='D'),
            'Discharges': [random.randint(15, 35) for _ in range(18)],
            'AI_Assisted': [random.randint(8, 25) for _ in range(18)]
        })
        
        # Discharge trends
        fig = px.line(discharge_data, x='Date', y=['Discharges', 'AI_Assisted'], 
                     title='Daily Discharge Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        # Efficiency metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Completion time distribution
            completion_times = [random.normalvariate(4.5, 1.2) for _ in range(50)]
            fig = px.histogram(x=completion_times, nbins=20, 
                             title='Discharge Completion Time Distribution (Hours)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Task completion rates
            task_data = {
                'Task': ['Vitals Check', 'Lab Results', 'Medication Review', 'Discharge Summary', 'Insurance', 'Transport'],
                'Completion Rate': [95, 88, 92, 78, 85, 90]
            }
            fig = px.bar(x=task_data['Task'], y=task_data['Completion Rate'],
                        title='Task Completion Rates (%)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("System Notifications")
        
        # Sample notifications
        notifications = [
            {"type": "success", "message": "Patient PT001 discharge summary completed", "time": "2 minutes ago"},
            {"type": "warning", "message": "Patient PT002 lab results pending", "time": "5 minutes ago"},
            {"type": "info", "message": "Transport team notified for PT003", "time": "10 minutes ago"},
            {"type": "success", "message": "Pharmacy approval received for PT003", "time": "15 minutes ago"},
        ]
        
        for notification in notifications:
            card_class = "success-card" if notification['type'] == 'success' else "alert-card"
            st.markdown(f"""
            <div class="{card_class}">
                <p><strong>{notification['message']}</strong></p>
                <small>{notification['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Notification settings
        st.subheader("Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("SMS Notifications", value=True)
            st.checkbox("Email Notifications", value=True)
            st.checkbox("WhatsApp Notifications", value=False)
        
        with col2:
            st.checkbox("Discharge Alerts", value=True)
            st.checkbox("Task Completion Alerts", value=True)
            st.checkbox("Emergency Notifications", value=True)

def simulate_ai_action(action_type):
    """Simulate AI agent actions"""
    if action_type == "discharge_summary":
        st.success("🤖 AI Agent: Generating discharge summary...")
        time.sleep(1)
        st.info("✅ Discharge summary generated and sent to physician for review")
    
    elif action_type == "staff_coordination":
        st.success("🤖 AI Agent: Coordinating with hospital staff...")
        time.sleep(1)
        st.info("✅ Notifications sent to nursing, pharmacy, and transport teams")
    
    elif action_type == "notifications":
        st.success("🤖 AI Agent: Processing notifications...")
        time.sleep(1)
        st.info("✅ SMS and email notifications sent to relevant staff members")

def simulate_ai_assistance(patient_id):
    """Simulate AI assistance for a specific patient"""
    patient = next((p for p in st.session_state.patients if p['id'] == patient_id), None)
    if patient:
        st.success(f"🤖 AI Agent assigned to assist with {patient['name']} ({patient_id})")
        
        # Simulate task completion
        incomplete_tasks = [task for task, status in patient['tasks'].items() if not status]
        if incomplete_tasks:
            # Complete one random task
            task_to_complete = random.choice(incomplete_tasks)
            patient['tasks'][task_to_complete] = True
            
            # Update completion percentage
            completed_count = sum(1 for status in patient['tasks'].values() if status)
            patient['checklist_completion'] = int((completed_count / len(patient['tasks'])) * 100)
            
            st.info(f"✅ AI completed task: {task_to_complete.replace('_', ' ').title()}")
        else:
            st.info("✅ All tasks completed for this patient!")

def show_patient_details(patient):
    """Show detailed patient information"""
    st.subheader(f"Patient Details: {patient['name']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Patient ID:** {patient['id']}")
        st.write(f"**Age:** {patient['age']}")
        st.write(f"**Room:** {patient['room']}")
        st.write(f"**Condition:** {patient['condition']}")
        st.write(f"**Doctor:** {patient['doctor']}")
    
    with col2:
        st.write(f"**Admission Date:** {patient['admission_date']}")
        st.write(f"**Estimated Discharge:** {patient['estimated_discharge']}")
        st.write(f"**Status:** {patient['discharge_status']}")
        st.write(f"**Priority:** {patient['priority']}")
    
    st.subheader("Task Checklist")
    for task, completed in patient['tasks'].items():
        status = "✅" if completed else "❌"
        st.write(f"{status} {task.replace('_', ' ').title()}")

if __name__ == "__main__":
    main()