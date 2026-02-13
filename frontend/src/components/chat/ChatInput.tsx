import React from 'react';
import { MdAttachFile, MdCode, MdMic, MdSend, MdStop } from 'react-icons/md';

interface ChatInputProps {
    input: string;
    setInput: (value: string) => void;
    handleSend: () => void;
    handleStop: () => void;
    loading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ input, setInput, handleSend, handleStop, loading }) => {
    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
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
    );
};

export default ChatInput;
