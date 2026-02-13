export interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    isStep?: boolean;
    step?: number;
    agent?: string;
    status?: 'running' | 'completed' | 'error' | 'stopped';
}

export interface OrchestratorEvent {
    type: 'start' | 'step_start' | 'step_complete' | 'plan_created' | 'error' | 'fatal_error' | 'final';
    task?: string;
    step?: number;
    agent?: string;
    result?: string;
    plan?: PlanStep[];
    error?: string;
}

export interface PlanStep {
    step: number;
    agent: string;
    task: string;
}

export interface Agent {
    name: string;
    ver: string;
    status: string;
    color: string;
    cpu: number | string;
    mem: number | string;
    role?: string;
}
