# Player Routing Brief — Nightlands Deployment Guidance (Pending GitHub Sync)

## 1. Purpose

Provide a unified checklist for directing human players (and co-play partners) to the Alfa or theatre where they add the most value. This script is invoked by High Command during pre-session briefings, Morningate observatory prompts, or in-client summoning.

## 2. Routing Criteria

1. **Operational Need:** Which front has the highest urgency? (Open incidents, stalled builds, delayed rituals.)
2. **Current Skillset:** What tooling or disciplines does the player actively maintain? (Translator ops, monitoring, narrative scripting.)
3. **Proven Strengths:** Historical performance from telemetry (successful missions, fast incident response, lore alignment score).
4. **Player Preference:** What do they enjoy? Capture self-reported preferences or recent opt-ins.

Weights are adjustable; default heuristic prioritises urgent needs first, then matches skill and enjoyment to minimise burnout.

## 3. Data Sources

| Signal | Location | Notes |
| --- | --- | --- |
| Operational backlog | `planning/incident_queue.md` (per workspace) | Tagged by urgency and required role |
| Skill registry | `logs/player_skill_index.json` (High Command) | Manual updates until automation lands |
| Performance telemetry | `exports/leaderboards/*.json` | Derived from gameplay exports and validation reports |
| Preference journal | `planning/player_preferences.md` | Optional submission; maintain privacy via Guardian filter |

## 4. Routing Flow

1. **Gather Signals:** Pull latest backlog tags, skill index, performance stats, and preferences.
2. **Score Options:** For each workspace/Alfa, compute a composite score using weighted criteria.
3. **Present Recommendation:** Surface top one or two deployments with rationale and urgency rating.
4. **Confirm Assignment:** Player accepts, negotiates, or requests alternate route; log decision in `planning/player_deployment_log.md`.
5. **Notify Workspace Lead:** Brief the receiving team and update Morningate “active fronts” display.

## 5. Automation Hooks

- Extend Morningate Reflection Layer to display “Call to Dawn” cards highlighting priority deployments.
- Embed a `python tools/player_router.py` (future) that reads the above data sources and prints the recommendation.
- Optionally integrate with safety watchers to nudge when a front stays under-staffed for >12 hours.

## 6. Guardian & War Office Alignment

- Guardian filter must approve language used in routing prompts (avoid coercion).
- War Office holds veto power for critical missions; final word logged in `war_office/orders/`.
- Maintain transparency: players can review why they were assigned to a given front.

## 7. Understaffed Front Response

When a front remains chronically understaffed:

1. **Assess the disguise:** Review narration, UI, and reward loops. Add lore framing or ritual flourishes so the work feels playful.
2. **Shift the balance:** Temporarily increase AI coverage or automate repetitive steps so humans aren’t forced into unfun roles while redesigns land.
3. **Log & iterate:** Capture the trend in `planning/player_deployment_log.md`, flag it to mission planners/War Office, and schedule a redesign sprint.

Continue routing humans there only when urgency demands it, while improving the experience to attract voluntary participation.

## 8. Pending Actions

- [ ] High Command to socialise this brief with Toyfoundry, Toysoldiers, Valiant Citadel, and R&D leads.
- [ ] Draft initial `player_skill_index.json` template and circulate for self-tagging.
- [ ] Define urgency scoring rubric (e.g., P0-P3) shared across workspaces.
- [ ] Plan Morningate UI card mockups for Call to Dawn feature.

*Status: Drafted locally; awaiting multi-front feedback and GitHub sync once access returns.*
