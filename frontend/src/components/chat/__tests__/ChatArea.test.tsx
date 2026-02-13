import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ChatArea from '../ChatArea';

// Mock dependencies
vi.mock('react-markdown', () => ({
    default: ({ children }) => <div data-testid="markdown">{children}</div>
}));

vi.mock('remark-gfm', () => ({
    default: () => { }
}));

vi.mock('react-syntax-highlighter', () => ({
    Prism: ({ children }) => <pre>{children}</pre>
}));

describe('ChatArea Component', () => {
    it('renders correctly', () => {
        render(<ChatArea title="Test Session" />);
        // Initial empty state
        expect(screen.getByText('Ready to orchestrate.')).toBeInTheDocument();
        expect(screen.getByText('Current Session: Test Session')).toBeInTheDocument();
    });

    it('updates input value', () => {
        render(<ChatArea />);
        const input = screen.getByPlaceholderText(/Type a command/i);
        fireEvent.change(input, { target: { value: 'Hello' } });
        expect(input.value).toBe('Hello');
    });
});
