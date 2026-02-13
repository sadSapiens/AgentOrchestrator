import React, { useState } from 'react';
import './Sidebar.css';
import Modal from './Modal';
import { MdSpaceDashboard, MdPeople, MdBolt, MdLink, MdSettings, MdClose } from 'react-icons/md';
import { FaAtom } from 'react-icons/fa';

const Sidebar = ({ currentView, setCurrentView, agents, onStopAll, onDeploy, onDelete }) => {
    const [isStopModalOpen, setStopModalOpen] = useState(false);
    const [isDeployModalOpen, setDeployModalOpen] = useState(false);
    const [deployName, setDeployName] = useState("");
    const [deployRole, setDeployRole] = useState("");

    const navItems = [
        { name: "Dashboard", icon: MdSpaceDashboard },
        { name: "Agents", icon: MdPeople },
        { name: "Workflows", icon: MdBolt },
        { name: "Integrations", icon: MdLink },
        { name: "Settings", icon: MdSettings },
    ];

    const handleDeploy = () => {
        setDeployName("");
        setDeployRole("");
        setDeployModalOpen(true);
    };

    const confirmDeploy = () => {
        if (onDeploy) {
            onDeploy({ name: deployName, role: deployRole });
        }
    };

    const handleStopAll = () => {
        setStopModalOpen(true);
    };

    return (
        <aside className="sidebar">
            {/* 1. Header */}
            <div className="sidebar-logo">
                <FaAtom className="logo-icon" style={{ color: 'var(--accent-purple)' }} />
                <span className="logo-text">AGENT ORCHESTRATOR</span>
            </div>

            {/* 2. Navigation */}
            <div className="nav-container">
                {navItems.map((item) => (
                    <div
                        key={item.name}
                        className={`nav-item ${currentView === item.name ? 'active' : ''}`}
                        onClick={() => setCurrentView && setCurrentView(item.name)}
                    >
                        <item.icon className="nav-icon" /> {item.name}
                    </div>
                ))}
            </div>

            {/* 3. Active Agents */}
            <div className="section-header">Active Agents</div>
            <div className="agent-list">
                {agents.map((agent, index) => (
                    <div key={index} className="agent-card">
                        <div className="agent-header">
                            <div className="agent-identity">
                                <span
                                    className="status-dot"
                                    style={{
                                        backgroundColor: agent.color,
                                        boxShadow: `0 0 8px ${agent.color}`
                                    }}
                                ></span>
                                <span className="agent-name">{agent.name}</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <span className="agent-version">{agent.ver}</span>
                                <button
                                    className="delete-agent-btn"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDelete && onDelete(agent.name);
                                    }}
                                    title="Delete Agent"
                                >
                                    <MdClose />
                                </button>
                            </div>
                        </div>
                        <div className="agent-status-text" style={{ color: agent.color }}>
                            {agent.status}
                        </div>

                        {/* CPU Bar */}
                        <div className="resource-row">
                            <span className="res-label">CPU</span>
                            <div className="progress-bg">
                                <div
                                    className="progress-fill"
                                    style={{
                                        width: `${agent.cpu}%`,
                                        backgroundColor: agent.color
                                    }}
                                ></div>
                            </div>
                            <span className="res-val">{agent.cpu}%</span>
                        </div>

                        {/* MEM Bar */}
                        <div className="resource-row">
                            <span className="res-label">MEM</span>
                            <div className="progress-bg">
                                <div
                                    className="progress-fill"
                                    style={{
                                        width: `${agent.mem * 10}%`,
                                        backgroundColor: agent.color
                                    }}
                                ></div>
                            </div>
                            <span className="res-val">{agent.mem}G</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* 4. Footer Actions */}
            <div className="sidebar-footer">
                <button className="custom-btn deploy-btn" onClick={handleDeploy}>Deploy New Agent</button>
                <button className="custom-btn stop-btn" onClick={handleStopAll}>Stop All</button>
            </div>
            <Modal
                isOpen={isStopModalOpen}
                onClose={() => setStopModalOpen(false)}
                title="Stop All Agents"
                confirmText="Stop"
                isDanger={true}
                onConfirm={onStopAll}
            >
                Are you sure you want to stop all active agents? This action cannot be undone and will terminate all running processes.
            </Modal>

            {/* Deploy Modal */}
            <Modal
                isOpen={isDeployModalOpen}
                onClose={() => setDeployModalOpen(false)}
                title="Deploy New Agent"
                confirmText="Deploy"
                onConfirm={confirmDeploy}
            >
                <div className="form-group">
                    <label>Agent Name</label>
                    <input
                        type="text"
                        className="modal-input"
                        placeholder="e.g. Code Reviewer"
                        value={deployName}
                        onChange={(e) => setDeployName(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label>Role Prompt</label>
                    <textarea
                        className="modal-textarea"
                        placeholder="Describe the agent's role and responsibilities..."
                        rows={4}
                        value={deployRole}
                        onChange={(e) => setDeployRole(e.target.value)}
                    />
                </div>
            </Modal>
        </aside>
    );
};

export default Sidebar;
