import React, { useState } from 'react';
import './ChatArea.css';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import { useOrchestrator } from '../../hooks/useOrchestrator';

interface ChatAreaProps {
    title?: string;
}

const ChatArea: React.FC<ChatAreaProps> = ({ title }) => {
    const { messages, loading, handleSend, handleStop } = useOrchestrator();
    const [input, setInput] = useState("");

    const onSend = () => {
        handleSend(input);
        setInput("");
    };

    return (
        <main className="chat-area">
            {/* Header */}
            <header className="chat-header">
                <div className="session-title">Current Session: {title || "Auto Orchestration"}</div>
                <div className="header-actions">
                    <button className="header-btn">Share</button>
                    <button className="header-btn primary-btn">New Chat</button>
                </div>
            </header>

            {/* Chat Content */}
            <MessageList messages={messages} />

            {/* Floating Input */}
            <ChatInput
                input={input}
                setInput={setInput}
                handleSend={onSend}
                handleStop={handleStop}
                loading={loading}
            />
        </main>
    );
};

export default ChatArea;
