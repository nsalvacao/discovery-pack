---
$schema: "../schemas/constraints-nfr.schema.json"
project: "[Project Name]"
date: "YYYY-MM-DD"
metadata:
  generated_at: "2026-01-06T00:00:00Z"
  generated_by: "[AI Model]"
  discovery_pack_version: "2.0.0"
  validated: false

security:
  authentication:
    description: "[Who can access what, method (SSO/OAuth/API keys)]"
    tag: "CONSTRAINT"
  authorization:
    model: "[RBAC/ABAC]"
    description: "[Authorization approach]"
  data_protection:
    - requirement: "[PII handling]"
      tag: "CONSTRAINT"
    - requirement: "[Encryption at rest/transit]"
      tag: "CONSTRAINT"
  trust_model:
    trust_boundaries:
      - boundary: "internal_systems"
        classification: "trusted"
      - boundary: "user_input"
        classification: "untrusted"
    threats:
      - threat: "[Threat 1]"
        mitigation: "[Mitigation strategy]"

performance:
  response_time:
    - operation: "[API call]"
      target_p95: "[200ms]"
      max_acceptable: "[500ms]"
      measurement_point: "[Client/Server]"
  throughput:
    requests_per_second: "[Target]"
    concurrent_users: "[Target]"
    data_volume: "[Expected growth]"
  scalability:
    approach: "[Horizontal/Vertical]"
    constraints:
      - "[Geographic distribution needs]"
    tag: "CONSTRAINT"

availability:
  uptime:
    sla_target: "[99.9%]"
    acceptable_downtime: "[43min/month]"
    maintenance_windows: "[When/how often]"
  disaster_recovery:
    rto: "[Recovery Time Objective]"
    rpo: "[Recovery Point Objective]"
    backup_strategy: "[Approach]"
  fault_tolerance:
    single_point_of_failure: "[Acceptable? Mitigations?]"
    graceful_degradation: "[How system fails]"

observability:
  logging:
    retention: "[Duration]"
    levels: "[Debug/Info/Warn/Error strategy]"
    sensitive_data_policy: "[Redaction policy]"
    tag: "CONSTRAINT"
  metrics:
    - metric: "[Business metric]"
      rationale: "[Why it matters]"
    - metric: "[Technical metric]"
      rationale: "[Why it matters]"
  alerting:
    critical_threshold: "[Conditions]"
    warning_threshold: "[Conditions]"
  tracing:
    distributed_tracing: "[Yes/No + tool]"
    debug_mode: "[Who/when accessible]"

compatibility:
  browser_platform_support:
    supported:
      - "[Browser/Platform 1]"
    not_supported:
      - platform: "[Platform X]"
        rationale: "[Why not]"
    tag: "CONSTRAINT"
  api_versioning:
    strategy: "[Semantic versioning/date-based]"
    deprecation_policy: "[Notice period, migration path]"
  dependencies:
    - dependency: "[Service/library]"
      version: "[Version]"
      fallback: "[What if unavailable]"
      lock_in_risk: "medium"

operational:
  deployment:
    frequency: "[Target]"
    rollback_capability: "[Required? How fast?]"
    strategy: "[Blue-green/canary]"
    tag: "CONSTRAINT"
  maintenance:
    expected_burden: "[Hours/week]"
    on_call_required: "[Yes/No]"
    runbook_requirements: "[What to document]"
  cost:
    budget: "[Hard limit]"
    cost_per_user: "[Target]"
    infrastructure_ceiling: "[Acceptable range]"
    tag: "CONSTRAINT"

accessibility:
  standards:
    wcag_level: "[A/AA/AAA]"
    screen_reader: "[Required?]"
    keyboard_navigation: "[Required?]"
    tag: "CONSTRAINT"
  i18n:
    languages_supported:
      - "[Language 1]"
    rtl_support: "[Yes/No]"
    locale_formatting: "[Currency, dates]"
  ux_constraints:
    max_steps_critical_flow: "[Target]"
    mobile_breakpoints:
      - "[Breakpoint 1]"
    offline_capability: "[Needed? What works offline?]"
---

# Constraints & Non-Functional Requirements

**This template includes YAML frontmatter for validation and automation.**

The frontmatter above contains structured data that:
- ✅ Validates against JSON schema
- ✅ Categorizes constraints systematically
- ✅ Feeds into handoff generation
- ✅ Provides audit trail

Keep the markdown body below for human narrative and detailed analysis.

---

## Security & Privacy

### Authentication & Authorization
[CONSTRAINT/ASSUMPTION]
- Who can access what?
- Authentication method (SSO, OAuth, API keys)?
- Authorization model (RBAC, ABAC)?

### Data Protection
[CONSTRAINT]
- PII handling requirements
- Encryption at rest/transit
- Data retention policies
- GDPR/CCPA compliance needs

### Trust Model
[When system handles sensitive operations or cross-trust-boundary interactions]

**Trust Boundaries:**
- [Trusted: internal systems]
- [Untrusted: user input, third-party APIs]

**Threat Model:**
1. [Threat 1]: [Mitigation]
2. [Threat 2]: [Mitigation]

---

## Performance & Scalability

### Response Time Requirements
| Operation | Target | Max Acceptable | Measurement Point |
|-----------|--------|----------------|-------------------|
| [API call] | [e.g., 200ms p95] | [e.g., 500ms] | [Client/server] |

### Throughput Requirements
- Requests/second: [Target]
- Concurrent users: [Target]
- Data volume: [Expected growth]

### Scalability Constraints
[CONSTRAINT]
- Horizontal vs vertical scaling approach
- Geographic distribution needs
- Peak load scenarios

---

## Availability & Reliability

### Uptime Requirements
- SLA target: [e.g., 99.9%]
- Acceptable downtime: [e.g., 43min/month]
- Maintenance windows: [When/how often]

### Disaster Recovery
- RTO (Recovery Time Objective): [Target]
- RPO (Recovery Point Objective): [Target]
- Backup strategy: [Approach]

### Fault Tolerance
- Single point of failure: [Acceptable? Mitigations?]
- Graceful degradation strategy: [How system fails]

---

## Observability & Monitoring

### Logging Requirements
[CONSTRAINT]
- Log retention: [Duration]
- Log levels: [Debug/Info/Warn/Error strategy]
- Sensitive data in logs: [Redaction policy]

### Metrics & Alerting
**Key metrics to track:**
1. [Business metric]: [Why it matters]
2. [Technical metric]: [Why it matters]

**Alert thresholds:**
- Critical: [Conditions]
- Warning: [Conditions]

### Tracing & Debugging
- Distributed tracing needs: [Yes/No + tool]
- Debug mode accessibility: [Who/when]

---

## Compatibility & Integration

### Browser/Platform Support
[CONSTRAINT]
- Supported: [List versions/platforms]
- Not supported: [List + rationale]

### API Versioning
- Strategy: [Semantic versioning, date-based, etc.]
- Deprecation policy: [Notice period, migration path]

### Third-Party Dependencies
| Dependency | Version | Fallback Strategy | Lock-in Risk |
|------------|---------|-------------------|--------------|
| [Service/lib] | [Version] | [What if unavailable?] | [High/Med/Low] |

---

## Operational Constraints

### Deployment
[CONSTRAINT]
- Deployment frequency: [Target]
- Rollback capability: [Required? How fast?]
- Blue-green/canary: [Strategy]

### Maintenance
- Expected maintenance burden: [Hours/week]
- On-call requirements: [Needed?]
- Runbook requirements: [What to document]

### Cost Constraints
[CONSTRAINT]
- Budget: [Hard limit]
- Cost per user/transaction: [Target]
- Infrastructure cost ceiling: [Acceptable range]

---

## Accessibility & Usability

### Accessibility Standards
[CONSTRAINT]
- WCAG level: [A/AA/AAA]
- Screen reader support: [Required?]
- Keyboard navigation: [Required?]

### Internationalization (i18n)
- Languages supported: [List]
- RTL support needed: [Yes/No]
- Locale-specific formatting: [Currency, dates, etc.]

### User Experience Constraints
- Maximum steps for critical flow: [Target]
- Mobile responsiveness: [Required breakpoints]
- Offline capability: [Needed? What works offline?]
