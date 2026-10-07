# ZainCash Support Pipeline

This is a back-office pipeline for ZainCash support tickets written in Iraqi dialect. For each ticket it decides the category, sets a priority, extracts the key details, finds the matching transaction, routes the ticket to the right team, and drafts a reply for a person to approve. It is not a chatbot, and it never sends anything on its own. If it is unsure about a ticket, it escalates it to a person with a note.

Built for the **Agentic AI Challenge Iraq, Topic 06: Support Pipeline Automation**.

## How a ticket flows

```mermaid
flowchart TD
    A([Support tickets arrive<br/>paste · CSV/JSON upload · CLI batch]) --> B[Clean the text<br/>Arabic digits → 0-9, hide card numbers]
    B --> C[Jev reads the ticket<br/>category · priority · red flags<br/>picks amount, date, phone, transaction ID]
    C --> D{Is Jev confident?}
    D -- Yes --> G
    D -- No --> E[Gemini gives a second opinion<br/>asked 3 times]
    E --> F{Gemini confident<br/>and agrees?}
    F -- Yes --> G[Look up the transaction<br/>in ZainCash records]
    F -- No --> X

    G --> H[Route to the right team<br/>and set priority]
    H --> I{Any red flags?<br/>fraud · several issues · missing info<br/>transaction not found · amount mismatch}
    I -- Yes --> X
    I -- No --> J[AI agent drafts a reply in Iraqi Arabic<br/>using policy documents + transaction]

    J --> K{Draft passes safety checks?<br/>cites policy · no invented numbers<br/>never asks for OTP/PIN}
    K -- No --> X
    K -- Yes --> R[Ready for review]

    X[Escalate to a human<br/>with a short note explaining why] --> Q
    R --> Q[Support agent reviews<br/>Approve · Edit · Reject]
    Q --> Z([Agent sends the approved reply<br/>nothing is sent automatically])

    classDef terminal fill:#e8f5c8,stroke:#6b8f3c,color:#1a1a1a
    classDef decision fill:#d6ecff,stroke:#3b82f6,color:#1a1a1a
    classDef action fill:#efe6ff,stroke:#8b7cc9,color:#1a1a1a
    classDef escalate fill:#f8e6df,stroke:#c4a090,color:#1a1a1a

    class A,Z terminal
    class D,F,I,K decision
    class B,C,E,G,H,J,R action
    class X,Q escalate
```

Colours in the diagram:
- **Green:** where tickets come in and where they finish.
- **Blue:** decisions the pipeline makes.
- **Purple:** automatic steps.
- **Orange:** steps a person handles.

Every path ends with a person approving the reply.

## Models

| Model | What it does here |
|---|---|
| **Jev** (TypeSafe System One) | Fast, cheap classification. Its confidence scores are calibrated, and it picks extracted values directly from the ticket text, so it cannot invent them. |
| **Gemini** | Second opinion on uncertain tickets, fallback extraction, the drafting agent, and the embeddings used to search the knowledge base |

## Design

The full design is in [`docs/superpowers/specs/2026-10-07-support-pipeline-design.md`](docs/superpowers/specs/2026-10-07-support-pipeline-design.md).

## Status

Under construction. Setup instructions, evaluation results and the disclosure of every model and tool used will be added here as each part lands.
