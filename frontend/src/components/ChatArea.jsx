import React, { useState, useEffect, useRef } from 'react';
import './ChatArea.css';
import { MdSend, MdAttachFile, MdMic, MdCode, MdStop } from 'react-icons/md';
import { FaRobot, FaUser } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const ChatArea = ({ title }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);
    const abortControllerRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const [loading, setLoading] = useState(false);

    const handleStop = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
        }
        setLoading(false);
        setMessages(prev => [...prev, {
            role: 'assistant',
            content: '*Process stopped by user.*',
            status: 'stopped'
        }]);
    };

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMsg = input;
        const newMsg = { role: 'user', content: userMsg };
        setMessages(prev => [...prev, newMsg]);
        setInput("");
        setLoading(true);

        // Abort controller
        abortControllerRef.current = new AbortController();

        // Retrieve settings
        const provider = localStorage.getItem('llm_provider') || 'openai';
        const apiKeys = {
            openai: localStorage.getItem('openai_api_key'),
            anthropic: localStorage.getItem('anthropic_api_key'),
            gemini: localStorage.getItem('gemini_api_key'),
            mistral: localStorage.getItem('mistral_api_key')
        };

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    prompt: userMsg,
                    api_keys: apiKeys,
                    mode: "Auto Orchestration"
                }),
                signal: abortControllerRef.current.signal
            });

            if (!response.ok) {
                let errorMsg = 'Network response was not ok';
                try {
                    const errorData = await response.json();
                    if (errorData.error) errorMsg = errorData.error;
                } catch (e) {
                    // Ignore
                }
                throw new Error(errorMsg);
            }

            // Stream reading
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;
                const lines = buffer.split("\n\n");
                buffer = lines.pop(); // Keep incomplete line

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const jsonStr = line.slice(6);
                        try {
                            const event = JSON.parse(jsonStr);
                            handleStreamEvent(event);
                        } catch (e) {
                            console.error("Error parsing stream event:", e);
                        }
                    }
                }
            }

        } catch (error) {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            } else {
                console.error("Error:", error);
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: `Error: ${error.message}`
                }]);
            }
        } finally {
            setLoading(false);
            abortControllerRef.current = null;
        }
    };

    const handleStreamEvent = (event) => {
        setMessages(prev => {
            const newMsgs = [...prev];

            if (event.type === 'step_start') {
                newMsgs.push({
                    role: 'assistant',
                    isStep: true,
                    agent: event.agent,
                    content: `**Executing Step ${event.step}:** ${event.task}...`,
                    step: event.step,
                    status: 'running'
                });
            } else if (event.type === 'step_complete') {
                // Find the running step and update it
                // We search from end to find the corresponding step
                for (let i = newMsgs.length - 1; i >= 0; i--) {
                    if (newMsgs[i].isStep && newMsgs[i].step === event.step && newMsgs[i].agent === event.agent) {
                        newMsgs[i] = {
                            ...newMsgs[i],
                            // Combine task description and result for context
                            content: `**Step ${event.step} Completed (${event.agent})**\n\n${event.result}`,
                            status: 'completed'
                        };
                        break;
                    }
                }
                // If not found (e.g. parallel), append
            } else if (event.type === 'plan_created') {
                // Format plan as markdown
                const planMd = event.plan.map(p => `- **Step ${p.step}** (${p.agent}): ${p.task}`).join('\n');
                newMsgs.push({
                    role: 'assistant',
                    isStep: true,
                    agent: 'Coordinator',
                    content: `**Plan Created:**\n\n${planMd}`,
                    status: 'completed'
                });
            } else if (event.type === 'error') {
                newMsgs.push({
                    role: 'assistant',
                    isStep: true,
                    agent: event.agent || 'System',
                    content: `**Error:** ${event.error}`,
                    status: 'error'
                });
            } else if (event.type === 'final') {
                newMsgs.push({
                    role: 'assistant',
                    content: event.result
                });
            }
            return newMsgs;
        });
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Code block renderer
    const CodeBlock = ({ node, inline, className, children, ...props }) => {
        const match = /language-(\w+)/.exec(className || '');
        return !inline && match ? (
            <SyntaxHighlighter
                style={vscDarkPlus}
                language={match[1]}
                PreTag="div"
                {...props}
            >
                {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
        ) : (
            <code className={className} {...props}>
                {children}
            </code>
        );
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
            <div className={`chat-content ${messages.length === 0 ? 'empty' : ''}`}>
                {messages.length === 0 ? (
                    <div className="empty-state">
                        <span className="empty-icon">🤖</span>
                        <div className="empty-text">Ready to orchestrate.</div>
                    </div>
                ) : (
                    <div className="messages-list">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`message-card ${msg.role} ${msg.isStep ? 'step-message' : ''} ${msg.status === 'running' ? 'processing' : ''}`}>
                                <div className={`message-avatar ${msg.role === 'user' ? 'user-avatar' : 'bot-avatar'}`}>
                                    {msg.role === 'user' ? <FaUser size={14} /> : <FaRobot size={16} />}
                                </div>
                                <div className="message-body">
                                    <div className="message-sender">
                                        {msg.role === 'user' ? 'You' : (msg.agent ? `Orchestrator • ${msg.agent}` : 'Orchestrator')}
                                        {msg.status === 'running' && <span style={{ marginLeft: '8px', opacity: 0.7, fontSize: '0.8em' }}>Thinking...</span>}
                                    </div>
                                    <div className="message-text markdown-body">
                                        <ReactMarkdown
                                            children={msg.content}
                                            remarkPlugins={[remarkGfm]}
                                            components={{
                                                code: CodeBlock
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* Floating Input */}
            <div className="floating-input-container">
                <div className="input-glass-pill">
                    <button className="action-btn">
                        <MdAttachFile />
                    </button>
                    <textarea
                        className="chat-input"
                        placeholder="Type a command or query for your agents..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        rows={1}
                        disabled={loading}
                    // Simple auto-grow hack or fixed size for now
                    />
                    <div className="input-actions">
                        <button className="action-btn">
                            <MdCode />
                        </button>
                        <button className="action-btn">
                            <MdMic />
                        </button>
                        {loading ? (
                            <button className="action-btn stop-btn" onClick={handleStop} title="Stop Agent">
                                <MdStop />
                            </button>
                        ) : (
                            <button className="action-btn send-btn" onClick={handleSend} title="Send">
                                <MdSend />
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
};

export default ChatArea;
