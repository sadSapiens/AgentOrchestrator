import React, { useState, useEffect } from 'react';
// @ts-ignore
import Sidebar from './components/Sidebar';
import ChatArea from './components/chat/ChatArea';
// @ts-ignore
import Settings from './components/Settings';
import './index.css';
import { Agent } from './types';

function App() {
  const [currentView, setCurrentView] = useState("Agents");
  const [agents, setAgents] = useState<Agent[]>([
    { name: "Researcher", ver: "v1.4", status: "Starting...", color: "#5F6368", cpu: 0, mem: 0, role: "Researcher" },
  ]);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await fetch('/api/agents');
        if (res.ok) {
          const data = await res.json();
          const formatted: Agent[] = data.map((a: any) => ({
            name: a.name,
            ver: a.ver || "v1.0",
            status: a.status || "Idle",
            color: a.status === "Running" ? "#34A853" : (a.status === "Error" ? "#EA4335" : "#4285F4"),
            cpu: Math.floor(Math.random() * 30),
            mem: (Math.random() * 2).toFixed(1),
            role: a.role
          }));
          if (formatted.length > 0) setAgents(formatted);
        }
      } catch (e) {
        console.error("Failed to fetch agents", e);
      }
    };

    fetchAgents();
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  const stopAllAgents = () => {
    setAgents(prevAgents => prevAgents.map(agent => ({
      ...agent,
      status: "Stopped",
      color: "#5F6368",
      cpu: 0,
      mem: 0
    })));
  };

  const deployNewAgent = (agentData: any) => {
    const id = Math.floor(Math.random() * 9000) + 1000;
    const name = agentData?.name || `Agent-${id}`;

    const newAgent: Agent = {
      name: name,
      ver: "v1.0",
      status: "Starting",
      color: "#Fbbc04",
      cpu: 5,
      mem: 0.2,
      role: agentData?.role || "Generic Agent"
    };

    setAgents(prev => [...prev, newAgent]);

    setTimeout(() => {
      setAgents(prev => prev.map(a =>
        a.name === newAgent.name ? { ...a, status: "Running", color: "#34A853", cpu: Math.floor(Math.random() * 40) + 10, mem: 1.0 } : a
      ));
    }, 2000);
  };

  const deleteAgent = (agentName: string) => {
    setAgents(prev => prev.filter(a => a.name !== agentName));
  };

  return (
    <>
      <Sidebar
        currentView={currentView}
        setCurrentView={setCurrentView}
        agents={agents}
        onStopAll={stopAllAgents}
        onDeploy={deployNewAgent}
        onDelete={deleteAgent}
      />
      {currentView === "Settings" ? (
        <Settings />
      ) : (
        <ChatArea title={currentView} />
      )}
    </>
  );
}

export default App;
