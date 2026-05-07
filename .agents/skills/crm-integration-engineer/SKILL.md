---
name: crm-integration-engineer
description: Workspace skill for CRM integrations, backend automation, HubSpot, Bitrix24, APIs, webhooks, and integration architecture
---

# crm-integration-engineer

This workspace focuses on CRM integrations, backend automation, API communication, and webhook-based systems.

Primary platforms:
- HubSpot
- Bitrix24
- REST APIs
- OAuth2 integrations
- Webhooks
- AI chatbot workflows
- Automation systems

## Usage

Use this skill when working with:
- CRM integrations
- webhook processing
- API synchronization
- backend automation
- chatbot integrations
- HubSpot or Bitrix24 development
- data synchronization between systems

Apply these rules before implementing or modifying integrations.

## Development Behavior

Before writing code:
- first explain what already exists
- explain what will be changed
- explain why the change is needed

Do not immediately generate code without analysis.

If uncertain:
- ask instead of assuming

## Architecture Rules

Before implementing new integrations:
- inspect existing services
- inspect existing models
- inspect existing API routes
- inspect existing database structure

Avoid creating parallel integration flows.

Prefer extending existing architecture over introducing new patterns.

Keep integration logic centralized and reusable.

Avoid overengineering.

Prefer simple and stable architecture.

## Integration Rules

- Always analyze the existing integration flow before making changes.
- Preserve backward compatibility unless explicitly instructed otherwise.
- Do not change webhook payload structures without approval.
- Do not change CRM field mappings without confirmation.
- Reuse existing services and integration utilities whenever possible.

## API Best Practices

When implementing integrations:
- validate API responses
- handle request timeouts
- implement retries when appropriate
- add structured logging
- handle API rate limits
- prevent duplicate processing
- implement proper error handling
- verify response status codes before processing data

Design integrations to be idempotent whenever possible.

## Data Integrity Rules

Never silently change:
- CRM IDs
- external IDs
- object relationships
- synchronization logic

Always preserve mapping consistency between systems.

When syncing data:
- prevent duplicate records
- validate identifiers
- log synchronization failures

## HubSpot Rules

When working with HubSpot:
- preserve object relationships
- verify property mappings
- handle pagination properly
- respect API rate limits
- use official APIs and recommended practices
- avoid deprecated endpoints
- preserve pipeline and association logic

## Bitrix24 Rules

When working with Bitrix24:
- preserve webhook compatibility
- avoid breaking CRM automation
- preserve custom field mappings
- avoid changing entity structures without approval
- preserve existing business process logic

## Security

Never hardcode:
- tokens
- API keys
- secrets
- production URLs

Use environment variables for all credentials and configuration.

## Backend Rules

For Python/Django projects:
- use virtual environments
- follow Django best practices
- separate business logic from views/controllers
- use reusable service classes for integrations
- keep integration logic modular and maintainable

## Dependency Rules

Before installing packages:
- verify whether existing dependencies already solve the problem
- avoid unnecessary libraries

Do not upgrade dependencies without approval.

## Development Workflow

Before major changes:
- explain risks
- explain compatibility impact

After changes:
- verify imports
- check syntax
- verify integration flow consistency
- verify webhook compatibility
- verify API request/response handling

## Important Principle

Prioritize:
- reliability
- maintainability
- compatibility
- stability

Avoid unnecessary complexity.