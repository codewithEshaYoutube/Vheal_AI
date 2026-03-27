import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import uuid

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VHeal AI - Agentic Hospital Discharge Copilot",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "patients" not in st.session_state:
    st.session_state.patients = []
if "ai_agents" not in st.session_state:
    st.session_state.ai_agents = []
if "notifications" not in st.session_state:
    st.session_state.notifications = []


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER CLASSES & FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class AIAgent:
    def __init__(self, name, role, status="active"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.status = status
        self.current_task = None
        self.tasks_completed = 0

    def assign_task(self, task, patient_id):
        self.current_task = {"task": task, "patient_id": patient_id}
        self.status = "processing"

    def complete_task(self):
        self.tasks_completed += 1
        self.current_task = None
        self.status = "active"


def create_ai_agents():
    return [
        AIAgent("Summary Agent",      "Discharge Summary Generation"),
        AIAgent("Coordination Agent", "Staff Coordination"),
        AIAgent("Checklist Agent",    "Task Completion Monitoring"),
        AIAgent("Alert Agent",        "Notification Management"),
    ]


def initialize_sample_data():
    if not st.session_state.patients:
        st.session_state.patients = [
            {
                "id": "PT001", "name": "John Smith", "age": 68,
                "condition": "Post-surgical recovery", "room": "302A",
                "discharge_status": "Ready for Discharge", "doctor": "Dr. Sarah Johnson",
                "admission_date": "2024-12-15", "estimated_discharge": "2024-12-18",
                "checklist_completion": 85, "priority": "High",
                "tasks": {"vitals_check": True, "lab_results": True, "medication_review": True,
                          "discharge_summary": False, "insurance_approval": True, "transport_arranged": False}
            },
            {
                "id": "PT002", "name": "Maria Garcia", "age": 45,
                "condition": "Pneumonia treatment", "room": "215B",
                "discharge_status": "Pending Medical Review", "doctor": "Dr. Michael Chen",
                "admission_date": "2024-12-16", "estimated_discharge": "2024-12-19",
                "checklist_completion": 60, "priority": "Medium",
                "tasks": {"vitals_check": True, "lab_results": False, "medication_review": True,
                          "discharge_summary": False, "insurance_approval": True, "transport_arranged": False}
            },
            {
                "id": "PT003", "name": "Robert Wilson", "age": 72,
                "condition": "Cardiac monitoring", "room": "401C",
                "discharge_status": "Awaiting Pharmacy", "doctor": "Dr. Lisa Park",
                "admission_date": "2024-12-14", "estimated_discharge": "2024-12-18",
                "checklist_completion": 90, "priority": "High",
                "tasks": {"vitals_check": True, "lab_results": True, "medication_review": False,
                          "discharge_summary": True, "insurance_approval": True, "transport_arranged": True}
            },
        ]


def simulate_ai_action(action_type):
    if action_type == "discharge_summary":
        st.success("🤖 AI Agent: Generating discharge summary...")
        st.info("✅ Discharge summary generated and sent to physician for review")
    elif action_type == "staff_coordination":
        st.success("🤖 AI Agent: Coordinating with hospital staff...")
        st.info("✅ Notifications sent to nursing, pharmacy, and transport teams")
    elif action_type == "notifications":
        st.success("🤖 AI Agent: Processing notifications...")
        st.info("✅ SMS and email notifications sent to relevant staff members")


def simulate_ai_assistance(patient_id):
    patient = next((p for p in st.session_state.patients if p["id"] == patient_id), None)
    if patient:
        st.success(f"🤖 AI Agent assigned to assist with {patient['name']} ({patient_id})")
        incomplete = [t for t, s in patient["tasks"].items() if not s]
        if incomplete:
            task = random.choice(incomplete)
            patient["tasks"][task] = True
            done = sum(1 for s in patient["tasks"].values() if s)
            patient["checklist_completion"] = int((done / len(patient["tasks"])) * 100)
            st.info(f"✅ AI completed task: {task.replace('_', ' ').title()}")
        else:
            st.info("✅ All tasks completed for this patient!")


def show_patient_details(patient):
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
    for task, done in patient["tasks"].items():
        st.write(f"{'✅' if done else '❌'} {task.replace('_', ' ').title()}")


# ═══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE HTML  (entire landing page as a string — no external file needed)
# ═══════════════════════════════════════════════════════════════════════════════

LANDING_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>VHeal AI</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet"/>
<style>
:root,[data-theme="dark"]{--bg:#050c18;--surface:#091425;--surface2:#0d1c33;--border:rgba(0,180,255,0.12);--accent:#00b4ff;--accent2:#00ffc8;--accent3:#ff4f6d;--text:#d6eaf8;--muted:#5f85a8;--heading:#ffffff;--card:#0a1828;--nav-bg:rgba(5,12,24,0.97);--footer-bg:#020810;--grid:rgba(0,180,255,0.04);}
[data-theme="light"]{--bg:#f0f6ff;--surface:#e6f0fb;--surface2:#dceaf7;--border:rgba(0,120,200,0.15);--accent:#0077cc;--accent2:#00a88a;--accent3:#e0244a;--text:#1a3050;--muted:#5a7a99;--heading:#091830;--card:#ffffff;--nav-bg:rgba(240,246,255,0.97);--footer-bg:#dce8f5;--grid:rgba(0,120,200,0.05);}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:16px;line-height:1.7;overflow-x:hidden;transition:background .4s,color .4s;}
body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0;}
.orb{position:fixed;border-radius:50%;filter:blur(120px);pointer-events:none;z-index:0;animation:drift 18s ease-in-out infinite alternate;}
.orb-1{width:600px;height:600px;background:rgba(0,180,255,0.07);top:-200px;left:-200px;}
.orb-2{width:400px;height:400px;background:rgba(0,255,200,0.05);bottom:100px;right:-100px;animation-delay:-8s;}
.orb-3{width:300px;height:300px;background:rgba(255,79,109,0.04);top:40%;left:40%;animation-delay:-4s;}
@keyframes drift{from{transform:translate(0,0) scale(1);}to{transform:translate(40px,30px) scale(1.1);}}
.container{max-width:1160px;margin:0 auto;padding:0 32px;position:relative;z-index:1;}
section{padding:100px 0;}
h1,h2,h3,h4{font-family:'Syne',sans-serif;color:var(--heading);}

/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:18px 40px;display:flex;align-items:center;justify-content:space-between;background:var(--nav-bg);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);transition:background .4s;}
.nav-logo{font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:var(--heading);letter-spacing:-.02em;}
.nav-logo span{color:var(--accent);}
.nav-links{display:flex;gap:36px;list-style:none;}
.nav-links a{color:var(--muted);text-decoration:none;font-size:.88rem;font-weight:500;letter-spacing:.04em;text-transform:uppercase;transition:color .2s;}
.nav-links a:hover{color:var(--accent);}
.nav-right{display:flex;align-items:center;gap:16px;}

/* THEME TOGGLE */
.theme-toggle-wrap{display:flex;align-items:center;gap:10px;}
.theme-label{font-size:.72rem;font-weight:600;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;user-select:none;}
.theme-toggle{width:52px;height:28px;background:var(--surface2);border:1px solid var(--border);border-radius:50px;cursor:pointer;transition:background .4s,border-color .4s,box-shadow .3s;outline:none;appearance:none;-webkit-appearance:none;position:relative;}
.theme-toggle:hover{box-shadow:0 0 14px rgba(0,180,255,0.3);border-color:var(--accent);}
.theme-toggle::before{content:'';position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:var(--accent);transition:transform .4s cubic-bezier(.34,1.56,.64,1);box-shadow:0 2px 8px rgba(0,0,0,0.3);}
.theme-toggle::after{content:'🌙';position:absolute;top:50%;left:6px;transform:translateY(-50%);font-size:11px;line-height:1;pointer-events:none;}
[data-theme="light"] .theme-toggle::before{transform:translateX(24px);}
[data-theme="light"] .theme-toggle::after{content:'☀️';left:auto;right:6px;}

/* BUTTONS */
.nav-cta{background:var(--accent);color:#000;font-family:'Syne',sans-serif;font-weight:700;font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;padding:10px 22px;border-radius:6px;border:none;cursor:pointer;transition:background .2s,box-shadow .2s;}
[data-theme="light"] .nav-cta{color:#fff;}
.nav-cta:hover{background:var(--accent2);box-shadow:0 0 20px rgba(0,255,200,0.3);}
.btn-primary{background:var(--accent);color:#000;font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;padding:14px 30px;border-radius:8px;border:none;cursor:pointer;letter-spacing:.03em;transition:all .25s;display:inline-flex;align-items:center;gap:8px;text-decoration:none;}
[data-theme="light"] .btn-primary{color:#fff;}
.btn-primary:hover{background:var(--accent2);box-shadow:0 0 30px rgba(0,255,200,0.35);transform:translateY(-2px);}
.btn-ghost{background:transparent;color:var(--text);font-family:'Syne',sans-serif;font-weight:600;font-size:.9rem;padding:13px 30px;border-radius:8px;text-decoration:none;border:1px solid var(--border);transition:all .25s;display:inline-flex;align-items:center;gap:8px;}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);}

/* HERO */
#hero{min-height:100vh;display:flex;align-items:center;padding-top:120px;position:relative;overflow:hidden;}
.hero-inner{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(0,180,255,0.1);border:1px solid rgba(0,180,255,0.25);border-radius:50px;padding:6px 16px;font-size:.78rem;color:var(--accent);letter-spacing:.08em;text-transform:uppercase;font-weight:600;margin-bottom:24px;}
.hero-badge::before{content:'';width:7px;height:7px;border-radius:50%;background:var(--accent);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,180,255,0.5);}50%{opacity:.6;box-shadow:0 0 0 6px rgba(0,180,255,0);}}
.hero-title{font-size:clamp(2.4rem,4.5vw,3.8rem);font-weight:800;line-height:1.1;letter-spacing:-.03em;margin-bottom:24px;}
.hero-title .line-accent{color:var(--accent);}
.hero-title .line-green{color:var(--accent2);}
.hero-desc{color:var(--muted);font-size:1.05rem;line-height:1.75;margin-bottom:36px;max-width:480px;}
.hero-btns{display:flex;gap:16px;flex-wrap:wrap;}
.hero-stats{display:flex;gap:32px;margin-top:48px;padding-top:32px;border-top:1px solid var(--border);}
.stat-num{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:var(--accent);line-height:1;}
.stat-label{font-size:.8rem;color:var(--muted);margin-top:4px;letter-spacing:.04em;}

/* DASHBOARD MOCKUP */
.hero-visual{position:relative;}
.dash-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;position:relative;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,0.2);}
.dash-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent2));}
.dash-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;}
.dash-title{font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;color:var(--heading);letter-spacing:.04em;text-transform:uppercase;}
.live-dot{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--accent2);font-weight:600;}
.live-dot::before{content:'';width:6px;height:6px;background:var(--accent2);border-radius:50%;animation:pulse 1.5s infinite;}
.patient-list{display:flex;flex-direction:column;gap:10px;}
.patient-row{display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:12px 16px;}
[data-theme="light"] .patient-row{background:rgba(0,0,0,0.03);border-color:rgba(0,0,0,0.06);}
.patient-name{font-size:.88rem;font-weight:500;color:var(--heading);}
.patient-ward{font-size:.75rem;color:var(--muted);}
.status-badge{font-size:.72rem;font-weight:700;padding:4px 10px;border-radius:20px;letter-spacing:.05em;text-transform:uppercase;}
.status-ready{background:rgba(0,255,200,0.12);color:var(--accent2);border:1px solid rgba(0,255,200,0.2);}
.status-pending{background:rgba(0,180,255,0.12);color:var(--accent);border:1px solid rgba(0,180,255,0.2);}
.status-alert{background:rgba(255,79,109,0.12);color:var(--accent3);border:1px solid rgba(255,79,109,0.2);}
.metric-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px;}
.metric-box{background:rgba(0,180,255,0.05);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center;}
.metric-val{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:var(--accent);}
.metric-lbl{font-size:.68rem;color:var(--muted);margin-top:2px;letter-spacing:.06em;text-transform:uppercase;}
.float-badge{position:absolute;bottom:-18px;right:24px;background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:12px 18px;display:flex;align-items:center;gap:10px;font-size:.82rem;font-weight:600;color:var(--heading);box-shadow:0 8px 30px rgba(0,0,0,0.2);animation:float 4s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}

/* SECTIONS */
#problem{background:linear-gradient(180deg,var(--bg) 0%,var(--surface) 100%);}
#features{background:var(--surface);}
#how{background:var(--bg);}
#tech{background:var(--surface);}
#team{background:var(--bg);}
#cta{background:linear-gradient(135deg,var(--surface),var(--surface2));text-align:center;padding:120px 0;position:relative;overflow:hidden;}
#cta::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 60% at 50% 50%,rgba(0,180,255,0.06),transparent 70%);}
#cta h2{font-size:clamp(2rem,4vw,3rem);font-weight:800;letter-spacing:-.03em;margin-bottom:20px;}
#cta p{color:var(--muted);max-width:500px;margin:0 auto 40px;font-size:1rem;}
#cta .hero-btns{justify-content:center;}
.section-label{font-size:.78rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:14px;}
.section-title{font-size:clamp(1.8rem,3vw,2.6rem);font-weight:800;letter-spacing:-.03em;line-height:1.15;margin-bottom:20px;}
.section-desc{color:var(--muted);max-width:580px;font-size:1rem;}
.features-header{text-align:center;margin-bottom:64px;}
.features-header .section-desc{margin:0 auto;}
.tech-header{text-align:center;margin-bottom:60px;}
.team-header{text-align:center;margin-bottom:60px;}

.problem-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:56px;}
.problem-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px;transition:transform .3s,border-color .3s;position:relative;overflow:hidden;}
.problem-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent3),transparent);opacity:0;transition:opacity .3s;}
.problem-card:hover{transform:translateY(-4px);border-color:rgba(255,79,109,0.3);}
.problem-card:hover::after{opacity:1;}
.problem-icon{font-size:2rem;margin-bottom:16px;}
.problem-card h4{font-size:1rem;font-weight:700;margin-bottom:10px;}
.problem-card p{font-size:.88rem;color:var(--muted);line-height:1.65;}

.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
.feat-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:32px 28px;transition:all .3s;position:relative;overflow:hidden;}
.feat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),transparent);opacity:0;transition:opacity .3s;}
.feat-card:hover{transform:translateY(-6px);border-color:rgba(0,180,255,0.3);box-shadow:0 20px 50px rgba(0,0,0,0.15);}
.feat-card:hover::before{opacity:1;}
.feat-icon{width:48px;height:48px;background:rgba(0,180,255,0.1);border:1px solid rgba(0,180,255,0.2);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;margin-bottom:20px;}
.feat-card h4{font-size:1rem;font-weight:700;margin-bottom:10px;}
.feat-card p{font-size:.87rem;color:var(--muted);line-height:1.65;}

.how-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;margin-top:56px;}
.steps{display:flex;flex-direction:column;}
.step{display:flex;gap:20px;padding-bottom:36px;}
.step:last-child{padding-bottom:0;}
.step-line{display:flex;flex-direction:column;align-items:center;}
.step-num{width:40px;height:40px;background:rgba(0,180,255,0.12);border:1px solid rgba(0,180,255,0.3);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:.85rem;color:var(--accent);flex-shrink:0;}
.step-connector{width:1px;flex:1;background:linear-gradient(to bottom,rgba(0,180,255,0.3),transparent);margin-top:8px;}
.step:last-child .step-connector{display:none;}
.step-body h4{font-size:.98rem;font-weight:700;margin-bottom:6px;color:var(--heading);}
.step-body p{font-size:.87rem;color:var(--muted);line-height:1.65;}
.terminal{background:#020a14;border:1px solid rgba(0,180,255,0.2);border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,0.3);}
.terminal-bar{background:var(--surface2);padding:10px 16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--border);}
.dot{width:10px;height:10px;border-radius:50%;}.dot-r{background:#ff5f57;}.dot-y{background:#ffbd2e;}.dot-g{background:#28c840;}
.terminal-title{font-size:.75rem;color:var(--muted);margin-left:8px;font-family:monospace;}
.terminal-body{padding:20px 24px;font-family:'Courier New',monospace;font-size:.8rem;line-height:2;}
.t-line{display:flex;gap:8px;}
.t-prompt{color:var(--accent2);}.t-cmd{color:#d6eaf8;}.t-out{color:#5f85a8;padding-left:16px;}.t-success{color:var(--accent2);padding-left:16px;}.t-warn{color:#ffd700;padding-left:16px;}
.cursor{display:inline-block;width:8px;height:14px;background:var(--accent);animation:blink 1s step-end infinite;vertical-align:text-bottom;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:0;}}

.tech-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;}
.tech-pill{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:20px 12px;text-align:center;transition:all .25s;cursor:default;}
.tech-pill:hover{border-color:var(--accent);background:rgba(0,180,255,0.05);transform:translateY(-3px);}
.tech-pill .t-icon{font-size:1.5rem;margin-bottom:8px;}
.tech-pill .t-name{font-size:.78rem;font-weight:600;color:var(--text);letter-spacing:.04em;}
.tech-pill .t-layer{font-size:.68rem;color:var(--muted);margin-top:3px;}

.team-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
.team-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px 24px;text-align:center;transition:all .3s;}
.team-card:hover{transform:translateY(-4px);border-color:rgba(0,180,255,0.3);}
.team-avatar{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:1.2rem;color:#fff;margin:0 auto 16px;}
.team-card h4{font-size:.98rem;font-weight:700;color:var(--heading);margin-bottom:4px;}
.team-role{font-size:.8rem;color:var(--accent);margin-bottom:6px;font-weight:600;}
.team-id{font-size:.75rem;color:var(--muted);font-family:monospace;}
.hack-banner{margin-top:60px;background:linear-gradient(135deg,rgba(0,180,255,0.08),rgba(0,255,200,0.05));border:1px solid rgba(0,180,255,0.2);border-radius:16px;padding:36px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;}
.hack-left h3{font-size:1.4rem;font-weight:800;margin-bottom:6px;}
.hack-left p{color:var(--muted);font-size:.9rem;}
.hack-badges{display:flex;gap:12px;flex-wrap:wrap;}
.hack-badge{background:rgba(0,255,200,0.1);border:1px solid rgba(0,255,200,0.25);color:var(--accent2);border-radius:8px;padding:8px 16px;font-size:.82rem;font-weight:700;letter-spacing:.04em;}

footer{background:var(--footer-bg);border-top:1px solid var(--border);padding:40px 0;text-align:center;font-size:.82rem;color:var(--muted);}
footer a{color:var(--accent);text-decoration:none;}

.fade-up{opacity:0;transform:translateY(30px);transition:opacity .7s ease,transform .7s ease;}
.fade-up.visible{opacity:1;transform:translateY(0);}

@media(max-width:900px){
  .hero-inner,.how-grid{grid-template-columns:1fr;}
  .features-grid,.problem-grid,.team-grid{grid-template-columns:1fr 1fr;}
  .tech-grid{grid-template-columns:repeat(3,1fr);}
  .hero-visual{display:none;}
  nav .nav-links{display:none;}
  .theme-label{display:none;}
}
@media(max-width:600px){
  .features-grid,.problem-grid,.team-grid{grid-template-columns:1fr;}
  .tech-grid{grid-template-columns:repeat(2,1fr);}
  nav{padding:14px 20px;}
}
</style>
</head>
<body>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>

<nav>
  <div class="nav-logo">V<span>Heal</span> AI</div>
  <ul class="nav-links">
    <li><a href="#problem">Problem</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#how">How It Works</a></li>
    <li><a href="#tech">Stack</a></li>
    <li><a href="#team">Team</a></li>
  </ul>
  <div class="nav-right">
    <div class="theme-toggle-wrap">
      <span class="theme-label" id="themeLabel">Dark</span>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme"></button>
    </div>
    <button class="nav-cta" onclick="goToApp()">Live Demo →</button>
  </div>
</nav>

<section id="hero">
  <div class="container">
    <div class="hero-inner">
      <div>
        <div class="hero-badge">🏆 Top 5 Global · Raise Your Hack Paris 2025</div>
        <h1 class="hero-title">Agentic AI for<br><span class="line-accent">Hospital Discharge</span><br><span class="line-green">Coordination</span></h1>
        <p class="hero-desc">VHeal AI is a fully autonomous discharge co-pilot that detects patient readiness, delegates tasks across departments, and sends real-time alerts — no manual handoffs needed.</p>
        <div class="hero-btns">
          <button class="btn-primary" onclick="goToApp()">▶ Live Demo</button>
          <a href="https://github.com/codewithEshaYoutube/Vheal_AI" target="_blank" class="btn-ghost">⬡ GitHub</a>
        </div>
        <div class="hero-stats">
          <div><div class="stat-num">923</div><div class="stat-label">Teams Globally</div></div>
          <div><div class="stat-num">Top 5</div><div class="stat-label">Final Placement</div></div>
          <div><div class="stat-num">72hr</div><div class="stat-label">Built In</div></div>
          <div><div class="stat-num">6</div><div class="stat-label">Team Members</div></div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="dash-card">
          <div class="dash-header"><span class="dash-title">Discharge Agent Dashboard</span><span class="live-dot">Live</span></div>
          <div class="patient-list">
            <div class="patient-row"><div><div class="patient-name">Sarah M. — Room 214</div><div class="patient-ward">Cardiology · Dr. Hasan</div></div><span class="status-badge status-ready">Ready</span></div>
            <div class="patient-row"><div><div class="patient-name">Ahmed K. — Room 308</div><div class="patient-ward">Orthopedics · Dr. Nadia</div></div><span class="status-badge status-pending">In Progress</span></div>
            <div class="patient-row"><div><div class="patient-name">Zara T. — Room 119</div><div class="patient-ward">Neurology · Dr. Malik</div></div><span class="status-badge status-alert">Alert Sent</span></div>
          </div>
          <div class="metric-strip">
            <div class="metric-box"><div class="metric-val">12</div><div class="metric-lbl">Pending</div></div>
            <div class="metric-box"><div class="metric-val">94%</div><div class="metric-lbl">Accuracy</div></div>
            <div class="metric-box"><div class="metric-val">3.2h</div><div class="metric-lbl">Avg Time</div></div>
          </div>
        </div>
        <div class="float-badge"><span>🤖</span> Agent delegated billing alert</div>
      </div>
    </div>
  </div>
</section>

<section id="problem">
  <div class="container">
    <div class="fade-up">
      <div class="section-label">The Problem</div>
      <h2 class="section-title">Discharge is Broken.<br>We Fixed It.</h2>
      <p class="section-desc">In major hospitals, discharge delays cascade into bed shortages, staff burnout, and rising patient costs — all caused by fragmented, manual workflows.</p>
    </div>
    <div class="problem-grid">
      <div class="problem-card fade-up"><div class="problem-icon">🏥</div><h4>Bed Shortages</h4><p>Delayed discharges block new admissions, creating critical capacity crises during peak hours.</p></div>
      <div class="problem-card fade-up"><div class="problem-icon">😫</div><h4>Staff Burnout</h4><p>Nurses and doctors spend hours on manual coordination instead of direct patient care.</p></div>
      <div class="problem-card fade-up"><div class="problem-icon">💸</div><h4>Higher Costs</h4><p>Inefficient handoffs between pharmacy, billing, and transport inflate costs for hospitals and patients.</p></div>
    </div>
  </div>
</section>

<section id="features">
  <div class="container">
    <div class="features-header fade-up">
      <div class="section-label">Core Features</div>
      <h2 class="section-title">Not Reactive. Not Rule-Based.<br>Truly Autonomous.</h2>
      <p class="section-desc">VHeal AI operates as a digital hospital staff member — reasoning, delegating, and communicating across every department.</p>
    </div>
    <div class="features-grid">
      <div class="feat-card fade-up"><div class="feat-icon">📍</div><h4>Discharge Detection</h4><p>Automatically triggers when a patient is marked ready — validating vitals, medications, labs, and required signatures.</p></div>
      <div class="feat-card fade-up"><div class="feat-icon">🧾</div><h4>AI-Generated Summaries</h4><p>Produces structured discharge summaries powered by GPT-4o, Claude 3, and Mistral — contextual and accurate.</p></div>
      <div class="feat-card fade-up"><div class="feat-icon">📞</div><h4>Smart Dept. Alerts</h4><p>Sends WhatsApp, email, and SMS notifications to pharmacy, billing, transport, and nursing automatically.</p></div>
      <div class="feat-card fade-up"><div class="feat-icon">📊</div><h4>Live Dashboard</h4><p>Real-time visibility into every agent action, staff update, and discharge stage across all active patients.</p></div>
      <div class="feat-card fade-up"><div class="feat-icon">🧠</div><h4>Multi-Agent Planning</h4><p>CrewAI + LangChain orchestration enables multi-step reasoning and task delegation across specialized agents.</p></div>
      <div class="feat-card fade-up"><div class="feat-icon">📆</div><h4>Discharge Scheduling</h4><p>Coordinates room availability, transport booking, and staff calendars to execute discharges without friction.</p></div>
    </div>
  </div>
</section>

<section id="how">
  <div class="container">
    <div class="fade-up">
      <div class="section-label">How It Works</div>
      <h2 class="section-title">From Trigger to Discharge<br>in Minutes</h2>
    </div>
    <div class="how-grid">
      <div class="steps fade-up">
        <div class="step"><div class="step-line"><div class="step-num">01</div><div class="step-connector"></div></div><div class="step-body"><h4>Patient Marked Ready</h4><p>Doctor marks patient "Ready for Discharge" in the EMR. VHeal AI triggers autonomously.</p></div></div>
        <div class="step"><div class="step-line"><div class="step-num">02</div><div class="step-connector"></div></div><div class="step-body"><h4>Multi-Step Validation</h4><p>Agent validates vitals, pending labs, medication clearances, and required signatures via API calls.</p></div></div>
        <div class="step"><div class="step-line"><div class="step-num">03</div><div class="step-connector"></div></div><div class="step-body"><h4>Department Coordination</h4><p>Delegates tasks to pharmacy, billing, transport, and nursing via WhatsApp, email, and SMS.</p></div></div>
        <div class="step"><div class="step-line"><div class="step-num">04</div><div class="step-connector"></div></div><div class="step-body"><h4>Summary Generation</h4><p>GPT-4o generates a complete discharge summary and sends it to the patient's portal.</p></div></div>
        <div class="step"><div class="step-line"><div class="step-num">05</div><div class="step-connector"></div></div><div class="step-body"><h4>Patient Discharged</h4><p>Bed is marked available, analytics updated, all staff notified. Zero manual steps.</p></div></div>
      </div>
      <div class="terminal fade-up">
        <div class="terminal-bar"><span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span><span class="terminal-title">vheal-agent · discharge_flow.py</span></div>
        <div class="terminal-body">
          <div class="t-line"><span class="t-prompt">→</span><span class="t-cmd">agent.trigger(patient_id="P2024")</span></div>
          <div class="t-line"><span class="t-out">✦ Checking vitals... OK</span></div>
          <div class="t-line"><span class="t-out">✦ Validating labs... OK</span></div>
          <div class="t-line"><span class="t-out">✦ Medication clearance... OK</span></div>
          <div class="t-line"><span class="t-warn">⚠ Billing signature pending</span></div>
          <div class="t-line"><span class="t-prompt">→</span><span class="t-cmd">notify("billing", channel="whatsapp")</span></div>
          <div class="t-line"><span class="t-success">✓ Alert sent to billing dept.</span></div>
          <div class="t-line"><span class="t-prompt">→</span><span class="t-cmd">generate_summary(model="gpt-4o")</span></div>
          <div class="t-line"><span class="t-success">✓ Summary generated (1.4s)</span></div>
          <div class="t-line"><span class="t-prompt">→</span><span class="t-cmd">discharge.complete()</span></div>
          <div class="t-line"><span class="t-success">✓ Patient P2024 discharged</span></div>
          <div class="t-line"><span class="t-prompt">$</span><span class="t-cmd"><span class="cursor"></span></span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="tech">
  <div class="container">
    <div class="tech-header fade-up"><div class="section-label">Technology Stack</div><h2 class="section-title">Built With Best-in-Class AI Infrastructure</h2></div>
    <div class="tech-grid fade-up">
      <div class="tech-pill"><div class="t-icon">🤖</div><div class="t-name">GPT-4o</div><div class="t-layer">LLM</div></div>
      <div class="tech-pill"><div class="t-icon">🧠</div><div class="t-name">Claude 3</div><div class="t-layer">LLM</div></div>
      <div class="tech-pill"><div class="t-icon">🔗</div><div class="t-name">LangChain</div><div class="t-layer">Agents</div></div>
      <div class="tech-pill"><div class="t-icon">👥</div><div class="t-name">CrewAI</div><div class="t-layer">Multi-Agent</div></div>
      <div class="tech-pill"><div class="t-icon">⚡</div><div class="t-name">FastAPI</div><div class="t-layer">Backend</div></div>
      <div class="tech-pill"><div class="t-icon">⚛️</div><div class="t-name">React.js</div><div class="t-layer">Frontend</div></div>
      <div class="tech-pill"><div class="t-icon">🍃</div><div class="t-name">MongoDB</div><div class="t-layer">Database</div></div>
      <div class="tech-pill"><div class="t-icon">🔥</div><div class="t-name">Firebase</div><div class="t-layer">Realtime DB</div></div>
      <div class="tech-pill"><div class="t-icon">📱</div><div class="t-name">Twilio</div><div class="t-layer">Messaging</div></div>
      <div class="tech-pill"><div class="t-icon">🌊</div><div class="t-name">Streamlit</div><div class="t-layer">Dashboard</div></div>
    </div>
  </div>
</section>

<section id="team">
  <div class="container">
    <div class="team-header fade-up"><div class="section-label">The Team</div><h2 class="section-title">Team VHeal</h2></div>
    <div class="team-grid fade-up">
      <div class="team-card"><div class="team-avatar">ET</div><h4>Eesha Tariq</h4><div class="team-role">AI Engineer</div><div class="team-id">Agent Logic · LLMs</div></div>
      <div class="team-card"><div class="team-avatar">AM</div><h4>Aroob Mushtaq</h4><div class="team-role">Backend Dev</div><div class="team-id">API Integration</div></div>
      <div class="team-card"><div class="team-avatar">AT</div><h4>Arfa Tariq</h4><div class="team-role">Researcher</div><div class="team-id">Clinical Workflows</div></div>
      <div class="team-card"><div class="team-avatar">ZT</div><h4>Zeeshan Tariq</h4><div class="team-role">Data Scientist</div><div class="team-id">RAG · Planning</div></div>
      <div class="team-card"><div class="team-avatar">WA</div><h4>Waqar Ahmed</h4><div class="team-role">Frontend Engineer</div><div class="team-id">Dashboards</div></div>
      <div class="team-card"><div class="team-avatar">SB</div><h4>Sujal Bedre</h4><div class="team-role">Prompt Engineer</div><div class="team-id">LLM Pipelines</div></div>
    </div>
    <div class="hack-banner fade-up">
      <div class="hack-left"><h3>🏆 Raise Your Hack 2025 — Paris</h3><p>Competed against 923 global teams. Built and deployed in under 72 hours.</p></div>
      <div class="hack-badges"><span class="hack-badge">Top 5 Global</span><span class="hack-badge">Onsite · Paris</span><span class="hack-badge">LabLab.ai</span></div>
    </div>
  </div>
</section>

<section id="cta">
  <div class="container">
    <h2>Ready to See It in Action?</h2>
    <p>Experience autonomous hospital discharge coordination — live, no sign-up required.</p>
    <div class="hero-btns">
      <button class="btn-primary" onclick="goToApp()">▶ Launch Live Demo</button>
      <a href="https://github.com/codewithEshaYoutube/Vheal_AI" target="_blank" class="btn-ghost">⬡ View on GitHub</a>
    </div>
  </div>
</section>

<footer>
  <div class="container">
    <p>Built by <strong>Team VHeal</strong> · Raise Your Hack Paris 2025 &nbsp;·&nbsp;
      <a href="https://github.com/codewithEshaYoutube/Vheal_AI" target="_blank">GitHub</a>
    </p>
    <p style="margin-top:10px;font-size:.75rem;">© 2025 VHeal AI. Apache-2.0 License.</p>
  </div>
</footer>

<script>
  // ── Theme toggle ──
  const toggle = document.getElementById('themeToggle');
  const label  = document.getElementById('themeLabel');
  const html   = document.documentElement;
  try { applyTheme(localStorage.getItem('vheal-theme') || 'dark'); } catch(e) { applyTheme('dark'); }
  toggle.addEventListener('click', () => applyTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  function applyTheme(t) {
    html.setAttribute('data-theme', t);
    label.textContent = t === 'dark' ? 'Dark' : 'Light';
    try { localStorage.setItem('vheal-theme', t); } catch(e) {}
  }

  // ── Scroll reveal ──
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        e.target.parentElement?.querySelectorAll('.fade-up')
          .forEach((c, i) => setTimeout(() => c.classList.add('visible'), i * 100));
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));

  // ── Go to App ──
  // Uses window.location to set a query param that Streamlit can read
  function goToApp() {
    const url = new URL(window.parent.location.href);
    url.searchParams.set('page', 'app');
    window.parent.location.href = url.toString();
  }
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTING LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

# Check URL query params first (set by the JS goToApp() function)
params = st.query_params
if params.get("page") == "app":
    st.session_state.page = "app"
    st.query_params.clear()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: LANDING
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.page == "landing":

    # Hide all Streamlit chrome for a clean full-page experience
    st.markdown("""
    <style>
        #MainMenu, header, footer { visibility: hidden; }
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        [data-testid="stAppViewContainer"] { padding: 0; }
        section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    # Render the full landing page HTML
    components.html(LANDING_HTML, height=5800, scrolling=True)

    # ── Fallback button (visible below the iframe if JS routing fails) ──
    st.markdown("<div style='text-align:center;padding:16px;'>", unsafe_allow_html=True)
    if st.button("▶ Enter the App", type="primary"):
        st.session_state.page = "app"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
else:
    # Restore Streamlit chrome
    st.markdown("""
    <style>
        #MainMenu, header { visibility: visible; }
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem; border-radius: 10px; color: white;
            text-align: center; margin-bottom: 2rem;
        }
        .patient-card {
            background: #ADD8E6; padding: 1rem; border-radius: 10px;
            margin: 0.5rem 0; border-left: 4px solid #28a745; color: black;
        }
        .alert-card   { background:#fff3cd; padding:1rem; border-radius:10px; margin:.5rem 0; border-left:4px solid #ffc107; }
        .success-card { background:#d4edda; padding:1rem; border-radius:10px; margin:.5rem 0; border-left:4px solid #28a745; }
        .agent-status { display:inline-block; padding:.25rem .5rem; border-radius:15px; font-size:.8rem; font-weight:bold; }
        .agent-active      { background:#28a745; color:white; }
        .agent-processing  { background:#ffc107; color:black; }
        .agent-completed   { background:#6c757d; color:white; }
    </style>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        if st.button("🏠 Back to Landing Page"):
            st.session_state.page = "landing"
            st.rerun()

        st.header("🤖 AI Agent Control Panel")
        if st.button("🚀 Initialize AI Agents"):
            st.session_state.ai_agents = create_ai_agents()
            st.success("AI Agents initialized!")

        if st.session_state.ai_agents:
            st.subheader("Active Agents")
            for agent in st.session_state.ai_agents:
                st.markdown(f"""
                <div style="margin:.5rem 0;padding:.6rem;background:rgba(0,0,0,0.05);border-radius:8px;">
                    <strong>{agent.name}</strong><br>
                    <span class="agent-status agent-{agent.status}">{agent.status.upper()}</span><br>
                    <small>{agent.role}</small><br>
                    <small>Tasks completed: {agent.tasks_completed}</small>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.subheader("Quick Actions")
        if st.button("📝 Generate Discharge Summary"):
            simulate_ai_action("discharge_summary")
        if st.button("📞 Coordinate Staff"):
            simulate_ai_action("staff_coordination")
        if st.button("🔔 Send Notifications"):
            simulate_ai_action("notifications")
        if st.button("🔄 Refresh Data"):
            st.rerun()

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>🚑 VHeal AI - Agentic Hospital Discharge Copilot</h1>
        <p>Autonomous AI-powered discharge coordination for modern hospitals</p>
    </div>
    """, unsafe_allow_html=True)

    initialize_sample_data()

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Patients", len(st.session_state.patients))
    with c2:
        ready = sum(1 for p in st.session_state.patients if p["discharge_status"] == "Ready for Discharge")
        st.metric("Ready for Discharge", ready)
    with c3:
        avg = sum(p["checklist_completion"] for p in st.session_state.patients) / max(len(st.session_state.patients), 1)
        st.metric("Avg Checklist", f"{avg:.1f}%")
    with c4:
        active = len([a for a in st.session_state.ai_agents if a.status == "active"])
        st.metric("Active AI Agents", active)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Patient Dashboard", "🤖 AI Agent Activity", "📊 Analytics", "🔔 Notifications"])

    with tab1:
        st.subheader("Patient Discharge Status")
        for patient in st.session_state.patients:
            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                st.markdown(f"""<div class="patient-card">
                    <h4>{patient['name']} ({patient['id']})</h4>
                    <p><b>Age:</b> {patient['age']} | <b>Room:</b> {patient['room']}</p>
                    <p><b>Condition:</b> {patient['condition']}</p>
                    <p><b>Doctor:</b> {patient['doctor']}</p>
                    <p><b>Status:</b> {patient['discharge_status']}</p>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.progress(patient["checklist_completion"] / 100, text=f"Checklist: {patient['checklist_completion']}%")
                done = sum(1 for s in patient["tasks"].values() if s)
                st.write(f"Tasks: {done}/{len(patient['tasks'])}")
            with c3:
                colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                st.write(f"Priority: {colors.get(patient['priority'], '⚪')} {patient['priority']}")
                if st.button("🤖 AI Assist",    key=f"assist_{patient['id']}"):  simulate_ai_assistance(patient["id"])
                if st.button("📄 View Details", key=f"detail_{patient['id']}"):  show_patient_details(patient)

    with tab2:
        st.subheader("AI Agent Activity Log")
        if st.session_state.ai_agents:
            for agent in st.session_state.ai_agents:
                c1, c2 = st.columns([3, 1])
                with c1:
                    task_html = f"<p><b>Task:</b> {agent.current_task['task']} for {agent.current_task['patient_id']}</p>" if agent.current_task else ""
                    st.markdown(f"""<div style="padding:1rem;border-radius:8px;border:1px solid #ddd;margin:.5rem 0;">
                        <h4>🤖 {agent.name}</h4><p><b>Role:</b> {agent.role}</p>{task_html}
                    </div>""", unsafe_allow_html=True)
                with c2:
                    (st.success if agent.status == "active" else st.info)("Ready" if agent.status == "active" else "Idle")

        st.subheader("Recent AI Actions")
        for a in [
            ("2024-12-18 14:30", "Summary Agent",      "Generated discharge summary for PT001"),
            ("2024-12-18 14:25", "Coordination Agent", "Coordinated pharmacy pickup for PT003"),
            ("2024-12-18 14:20", "Alert Agent",        "Sent notification to transport team"),
            ("2024-12-18 14:15", "Checklist Agent",    "Updated task completion for PT002"),
        ]:
            st.markdown(f'<div class="success-card"><p><b>{a[0]}</b> — {a[1]}</p><p>{a[2]}</p></div>', unsafe_allow_html=True)

    with tab3:
        st.subheader("Hospital Discharge Analytics")
        df = pd.DataFrame({
            "Date": pd.date_range("2024-12-01", periods=18, freq="D"),
            "Discharges":  [random.randint(15, 35) for _ in range(18)],
            "AI_Assisted": [random.randint(8,  25) for _ in range(18)],
        })
        st.plotly_chart(px.line(df, x="Date", y=["Discharges", "AI_Assisted"], title="Daily Discharge Trends"), use_container_width=True)
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.histogram(x=[random.normalvariate(4.5, 1.2) for _ in range(50)], nbins=20, title="Completion Time (Hours)"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(x=["Vitals","Labs","Meds","Summary","Insurance","Transport"], y=[95,88,92,78,85,90], title="Task Completion Rates (%)"), use_container_width=True)

    with tab4:
        st.subheader("System Notifications")
        for n in [
            ("success", "Patient PT001 discharge summary completed", "2 minutes ago"),
            ("warning", "Patient PT002 lab results pending",          "5 minutes ago"),
            ("info",    "Transport team notified for PT003",          "10 minutes ago"),
            ("success", "Pharmacy approval received for PT003",       "15 minutes ago"),
        ]:
            card = "success-card" if n[0] == "success" else "alert-card"
            st.markdown(f'<div class="{card}"><p><b>{n[1]}</b></p><small>{n[2]}</small></div>', unsafe_allow_html=True)

        st.subheader("Notification Settings")
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("SMS Notifications",      value=True)
            st.checkbox("Email Notifications",    value=True)
            st.checkbox("WhatsApp Notifications", value=False)
        with c2:
            st.checkbox("Discharge Alerts",       value=True) 
            st.checkbox("Task Completion Alerts", value=True)
            st.checkbox("Emergency Notifications",value=True)
