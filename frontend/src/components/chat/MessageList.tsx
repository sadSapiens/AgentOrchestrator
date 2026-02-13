import React, { useRef, useEffect } from 'react';
import MessageItem from './MessageItem';
import { Message } from '../../types';

interface MessageListProps {
    messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    if (messages.length === 0) {
        return (
            <div className="chat-content empty">
                <div className="empty-state">
                    <span className="empty-icon">🤖</span>
                    <div className="empty-text">Ready to orchestrate.</div>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-content">
            <div className="messages-list">
                {messages.map((msg, idx) => (
                    <MessageItem key={idx} message={msg} />
                ))}
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
};

export default MessageList;
