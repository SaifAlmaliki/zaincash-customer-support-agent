# ZainCash support: architecture and ticket flow {#support-overview}

ZainCash support uses one Jev classification path, with deterministic routing and a human approval boundary.

- Jev is the only ticket classifier; uncertainty remains an escalation reason.[](source:graph)
- Gemini is limited to extraction gaps and optional drafting, not classification.[](source:factory)
- PostgreSQL, policy retrieval, and the drafting agent support the same ticket journey.[](source:readme)

@answer scope="Current repository · local runtime · Jev-only classification"
@meta locale=en quality_profile=showcase repo_url=https://github.com/SaifAlmaliki/zaincash-customer-support-agent.git repo_revision=8f8f6f5dcda6522d1a131a3c02b24a0f0f70835a
@source graph title="LangGraph ticket pipeline" path=backend/app/pipeline/graph.py lines=56:149
@source factory title="Pipeline model wiring" path=backend/app/pipeline/factory.py lines=34:117
@source rules title="Routing and escalation rules" path=backend/app/pipeline/stage5_decide/rules.py lines=45:81
@source api title="FastAPI batch entry point" path=backend/app/api/runs.py lines=30:67
@source readme title="Pipeline phases and model responsibilities" path=README.md lines=101:113

## 1 · System architecture {#system-architecture}

@architecture id=system-map title="Applications, pipeline, models, and review"
| entry | Web + CLI entry | frontend | source:api |
| pipeline | LangGraph | backend | source:graph |
| jev-service | Jev | cloud | source:factory |
| support-models | Support LLMs | cloud | source:factory |
| database | PostgreSQL | database | source:readme |
| reviewer | Human review | security | source:readme |
| entry > pipeline | tickets |
| pipeline > jev-service | classify |
| pipeline > support-models | extract + draft |
| pipeline > database | SQL + vectors |
| pipeline > reviewer | outcome |
| reviewer > database | audit |

## 2 · Ticket flow {#ticket-flow}

@workflow id=ticket-journey title="Jev-only processing and human approval"
| lane entry | Entry |
| lane process | Classification |
| lane resolution | Investigation + reply |
| lane control | Review |
| ticket | Ticket received | external | entry | source:api |
| prepare | Prepare text | backend | process | source:graph |
| text-check | Text present? | backend | process | source:graph |
| empty-review | Escalate empty | security | control | source:graph |
| jev-step-node | Jev classifies | cloud | process | source:graph |
| extract | Verify + fill fields | backend | process | source:graph |
| lookup | Match transaction | database | resolution | source:graph |
| decide | Apply routing rules | backend | resolution | source:rules |
| draft | Draft + safety checks | backend | resolution | source:graph |
| approve | Human approval | security | control | source:readme |
| ticket > prepare | |
| prepare > text-check | |
| text-check > empty-review | no |
| text-check > jev-step-node | yes |
| jev-step-node > extract | |
| extract > lookup | |
| lookup > decide | |
| decide > draft | reasons kept |
| draft > approve | |

@steps id=journey-notes
| prepare-note | Prepare text | Normalize text and mask card numbers. | ticket-journey | prepare |
| jev-note | Jev classifies | Only Jev classifies. Low confidence remains attached for escalation. | ticket-journey | jev-step-node |
| decide-note | Apply routing rules | Python rules set team, priority, and escalation reasons. | ticket-journey | decide |
| approve-note | Human approval | A person approves, edits, or rejects. Nothing is sent automatically. | ticket-journey | approve |
