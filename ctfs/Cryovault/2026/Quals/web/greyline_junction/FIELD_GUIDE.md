# Greyline Junction — operator card

Greyline Junction has two published control revisions. A route authority reserves track circuits for one train. The desk can change control revision once, before any train moves. A movement uses an authority ID issued by the planning desk.

Your task is to produce a valid incident record showing that the control desk authorized two movements which occupy the same physical track circuit. The incident register returns the event flag only when it verifies that contradiction from the desk's own sealed state.

The service is a fictional simulation. It has no connection to any real railway.

## Desk API

All write requests use JSON. The desk keeps no server-side session: `POST /api/reset` gives a sealed `state` token; send the latest token with each request. Each new desk session receives its own relabeled control board.

| Operation | Request body | Result |
| --- | --- | --- |
| `POST /api/reset` | `{}` | New state token, revision A |
| `POST /api/scheme` | `{"state":"..."}` | Current revision's route IDs, paths and flank circuits |
| `POST /api/plan` | `{"state":"...","train":"A12","route":"<listed route ID>"}` | Authority ID, held circuits, next state |
| `POST /api/cancel` | `{"state":"...","authority":"..."}` | Withdraw a planned authority and release its reservation |
| `POST /api/changeover` | `{"state":"..."}` | Revision B and next state; allowed once before movement |
| `POST /api/dispatch` | `{"state":"...","authority":"..."}` | Movement path and next state |
| `POST /api/incident` | `{"state":"..."}` | Incident result |

Inspect your service's scheme for its route IDs. Each desk session holds at most four authority cards. A train code is one capital letter followed by one or two digits. A card can be used once. A route cannot be planned if another live authority holds any required circuit or the shared approach lock.

The planning desk closes at changeover.

Track circuits detect whether a train occupies a section of rail; points determine which path a train takes. For real-world background, see [Network Rail's track-circuit explanation](https://www.networkrail.co.uk/stories/track-circuits-explained/) and [European Union Agency for Railways' incident-report guidance](https://www.era.europa.eu/system/files/2023-04/Guidance%20on%20railway%20accident%20and%20incident%20investigation%20reports_V1.0.pdf). Those sources explain terminology, not this fictional layout.

The flag format is `isfcr{...}`.
