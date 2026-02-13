import React, { useState, useEffect } from 'react';
import './Settings.css';
import { MdSettings, MdPsychology, MdPerson, MdPalette } from 'react-icons/md';

const Settings = () => {
    const [activeTab, setActiveTab] = useState("llm");

    // LLM State
    const [provider, setProvider] = useState(localStorage.getItem('llm_provider') || 'openai');
    const [openaiKey, setOpenaiKey] = useState(localStorage.getItem('openai_api_key') || "");
    const [anthropicKey, setAnthropicKey] = useState(localStorage.getItem('anthropic_api_key') || "");
    const [geminiKey, setGeminiKey] = useState(localStorage.getItem('gemini_api_key') || "");
    const [mistralKey, setMistralKey] = useState(localStorage.getItem('mistral_api_key') || "");
    const [maxTokens, setMaxTokens] = useState(Number(localStorage.getItem('max_tokens')) || 2048);

    // Profile State (Simulated)
    const [username, setUsername] = useState("User");
    const [email, setEmail] = useState("user@example.com");

    // General State
    const [autoScroll, setAutoScroll] = useState(true);
    const [notifications, setNotifications] = useState(false);

    // Theme State
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

    const [saved, setSaved] = useState(false);

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    const handleSave = () => {
        // Save LLM settings
        localStorage.setItem('llm_provider', provider);
        localStorage.setItem('openai_api_key', openaiKey);
        localStorage.setItem('anthropic_api_key', anthropicKey);
        localStorage.setItem('gemini_api_key', geminiKey);
        localStorage.setItem('mistral_api_key', mistralKey);
        localStorage.setItem('max_tokens', maxTokens);
        localStorage.setItem('theme', theme);

        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    const tabs = [
        { id: 'llm', label: 'LLM Configuration', icon: MdPsychology },
        { id: 'general', label: 'General', icon: MdSettings },
        { id: 'profile', label: 'Profile', icon: MdPerson },
        { id: 'appearance', label: 'Appearance', icon: MdPalette },
    ];

    return (
        <div className="settings-container">
            {/* Settings Sidebar */}
            <div className="settings-sidebar">
                <div style={{ padding: '0 0 20px 12px', fontSize: '1.1rem', fontWeight: 600, color: '#E3E3E3' }}>Settings</div>
                {tabs.map(tab => (
                    <div
                        key={tab.id}
                        className={`settings-nav-item ${activeTab === tab.id ? 'active' : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        <tab.icon size={20} />
                        {tab.label}
                    </div>
                ))}
            </div>

            {/* Main Content Area */}
            <div className="settings-main">
                {activeTab === 'llm' && (
                    <div className="animate-fade-in">
                        <div className="section-title">Model Settings</div>
                        <div className="section-desc">Configure the brain of your agents. Select your preferred AI provider.</div>

                        <div className="settings-card">
                            <div className="setting-group">
                                <label>AI Provider</label>
                                <select
                                    className="setting-input"
                                    value={provider}
                                    onChange={(e) => setProvider(e.target.value)}
                                >
                                    <option value="openai">OpenAI (GPT-4)</option>
                                    <option value="anthropic">Anthropic (Claude 3)</option>
                                    <option value="gemini">Google (Gemini Pro)</option>
                                    <option value="mistral">Mistral AI</option>
                                </select>
                            </div>

                            {provider === 'openai' && (
                                <div className="setting-group">
                                    <label>OpenAI API Key</label>
                                    <input
                                        type="password"
                                        className="setting-input"
                                        placeholder="sk-..."
                                        value={openaiKey}
                                        onChange={(e) => setOpenaiKey(e.target.value)}
                                    />
                                </div>
                            )}

                            {provider === 'anthropic' && (
                                <div className="setting-group">
                                    <label>Anthropic API Key</label>
                                    <input
                                        type="password"
                                        className="setting-input"
                                        placeholder="sk-ant-..."
                                        value={anthropicKey}
                                        onChange={(e) => setAnthropicKey(e.target.value)}
                                    />
                                </div>
                            )}

                            {provider === 'gemini' && (
                                <div className="setting-group">
                                    <label>Gemini API Key</label>
                                    <input
                                        type="password"
                                        className="setting-input"
                                        placeholder="AIza..."
                                        value={geminiKey}
                                        onChange={(e) => setGeminiKey(e.target.value)}
                                    />
                                </div>
                            )}

                            {provider === 'mistral' && (
                                <div className="setting-group">
                                    <label>Mistral API Key</label>
                                    <input
                                        type="password"
                                        className="setting-input"
                                        placeholder="mw-..."
                                        value={mistralKey}
                                        onChange={(e) => setMistralKey(e.target.value)}
                                    />
                                </div>
                            )}

                            <div className="setting-group">
                                <label>Max Tokens</label>
                                <input
                                    type="number"
                                    className="setting-input"
                                    value={maxTokens}
                                    onChange={(e) => setMaxTokens(Number(e.target.value))}
                                />
                                <span className="setting-desc">Maximum context window for agents.</span>
                            </div>

                            <button className="save-btn" onClick={handleSave}>
                                {saved ? "Saved!" : "Save Changes"}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'profile' && (
                    <div className="animate-fade-in">
                        <div className="section-title">Profile</div>
                        <div className="section-desc">Manage your personal information and account details.</div>
                        <div className="settings-card">
                            <div className="setting-group">
                                <label>Username</label>
                                <input
                                    type="text"
                                    className="setting-input"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>
                            <div className="setting-group">
                                <label>Email</label>
                                <input
                                    type="email"
                                    className="setting-input"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>
                            <button className="save-btn" onClick={() => setSaved(true)}>
                                {saved ? "Updated!" : "Update Profile"}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'general' && (
                    <div className="animate-fade-in">
                        <div className="section-title">General Settings</div>
                        <div className="section-desc">Manage global application behavior and notifications.</div>
                        <div className="settings-card">
                            <div className="setting-group checkbox-group">
                                <div className="setting-info">
                                    <label>Auto-scroll Chat</label>
                                    <span className="setting-desc">Automatically scroll to the bottom when new messages arrive.</span>
                                </div>
                                <input
                                    type="checkbox"
                                    checked={autoScroll}
                                    onChange={(e) => setAutoScroll(e.target.checked)}
                                />
                            </div>
                            <div className="setting-group checkbox-group">
                                <div className="setting-info">
                                    <label>Enable Notifications</label>
                                    <span className="setting-desc">Receive desktop alerts when agents require attention.</span>
                                </div>
                                <input
                                    type="checkbox"
                                    checked={notifications}
                                    onChange={(e) => setNotifications(e.target.checked)}
                                />
                            </div>
                            <button className="save-btn" onClick={() => setSaved(true)}>
                                {saved ? "Settings Saved!" : "Save Preferences"}
                            </button>
                        </div>
                    </div>
                )}

                {activeTab === 'appearance' && (
                    <div className="animate-fade-in">
                        <div className="section-title">Appearance</div>
                        <div className="section-desc">Customize the look and feel of the application.</div>

                        <div className="settings-card">
                            <label style={{ display: 'block', marginBottom: '16px', color: 'var(--text-muted)' }}>Theme</label>
                            <div className="theme-grid">
                                {['light', 'dark', 'blue', 'purple', 'green'].map((t) => (
                                    <div
                                        key={t}
                                        className={`theme-option ${theme === t ? 'active' : ''}`}
                                        onClick={() => setTheme(t)}
                                    >
                                        <div className={`theme-preview theme-${t}`}></div>
                                        <span>{t.charAt(0).toUpperCase() + t.slice(1)}</span>
                                    </div>
                                ))}
                            </div>

                            <button className="save-btn" onClick={handleSave}>
                                {saved ? "Applied!" : "Apply Theme"}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Settings;
