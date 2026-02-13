import { useState, useRef, useCallback } from 'react';
import { Message, OrchestratorEvent } from '../types';

export const useOrchestrator = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const abortControllerRef = useRef<AbortController | null>(null);

    const handleStop = useCallback(() => {
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
    }, []);

    const handleStreamEvent = useCallback((event: OrchestratorEvent) => {
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
                } as Message);
            } else if (event.type === 'step_complete') {
                // Find the running step and update it
                for (let i = newMsgs.length - 1; i >= 0; i--) {
                    if (newMsgs[i].isStep && newMsgs[i].step === event.step && newMsgs[i].agent === event.agent) {
                        newMsgs[i] = {
                            ...newMsgs[i],
                            content: `**Step ${event.step} Completed (${event.agent})**\n\n${event.result}`,
                            status: 'completed'
                        };
                        break;
                    }
                }
            } else if (event.type === 'plan_created') {
                const planMd = event.plan?.map(p => `- **Step ${p.step}** (${p.agent}): ${p.task}`).join('\n') || "";
                newMsgs.push({
                    role: 'assistant',
                    isStep: true,
                    agent: 'Coordinator',
                    content: `**Plan Created:**\n\n${planMd}`,
                    status: 'completed'
                } as Message);
            } else if (event.type === 'error') {
                newMsgs.push({
                    role: 'assistant',
                    isStep: true,
                    agent: event.agent || 'System',
                    content: `**Error:** ${event.error}`,
                    status: 'error'
                } as Message);
            } else if (event.type === 'final') {
                newMsgs.push({
                    role: 'assistant',
                    content: event.result || ""
                } as Message);
            }
            return newMsgs;
        });
    }, []);

    const handleSend = useCallback(async (prompt: string) => {
        if (!prompt.trim() || loading) return;

        const newMsg: Message = { role: 'user', content: prompt };
        setMessages(prev => [...prev, newMsg]);
        setLoading(true);

        // Abort controller
        abortControllerRef.current = new AbortController();

        // Retrieve settings
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
                    prompt,
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

            if (!response.body) throw new Error("No response body");

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
                buffer = lines.pop() || ""; // Keep incomplete line

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const jsonStr = line.slice(6);
                        try {
                            const event = JSON.parse(jsonStr) as OrchestratorEvent;
                            handleStreamEvent(event);
                        } catch (e) {
                            console.error("Error parsing stream event:", e);
                        }
                    }
                }
            }

        } catch (error: any) {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            } else {
                console.error("Error:", error);
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: `Error: ${error.message}`,
                    status: 'error'
                }]);
            }
        } finally {
            setLoading(false);
            abortControllerRef.current = null;
        }
    }, [loading, handleStreamEvent]);

    return { messages, loading, handleSend, handleStop };
};
