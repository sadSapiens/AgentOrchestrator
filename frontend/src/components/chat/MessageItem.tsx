import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { FaRobot, FaUser } from 'react-icons/fa';
import { Message } from '../../types';

interface MessageItemProps {
    message: Message;
}

const CodeBlock = ({ node, inline, className, children, ...props }: any) => {
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

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
    return (
        <div className={`message-card ${message.role} ${message.isStep ? 'step-message' : ''} ${message.status === 'running' ? 'processing' : ''}`}>
            <div className={`message-avatar ${message.role === 'user' ? 'user-avatar' : 'bot-avatar'}`}>
                {message.role === 'user' ? <FaUser size={14} /> : <FaRobot size={16} />}
            </div>
            <div className="message-body">
                <div className="message-sender">
                    {message.role === 'user' ? 'You' : (message.agent ? `Orchestrator • ${message.agent}` : 'Orchestrator')}
                    {message.status === 'running' && <span style={{ marginLeft: '8px', opacity: 0.7, fontSize: '0.8em' }}>Thinking...</span>}
                </div>
                <div className="message-text markdown-body">
                    <ReactMarkdown
                        children={message.content}
                        remarkPlugins={[remarkGfm]}
                        components={{
                            code: CodeBlock
                        }}
                    />
                </div>
            </div>
        </div>
    );
};

export default MessageItem;
