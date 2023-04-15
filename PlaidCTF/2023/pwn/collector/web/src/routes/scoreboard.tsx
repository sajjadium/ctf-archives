import { For, Index, Show, Suspense } from "solid-js";
import { useRouteData } from "solid-start";
import { createServerData$ } from "solid-start/server";
import sql from "~/db";
import { requireUserId } from "~/db/session";

type ScoreboardEntry = {
  username: string;
  distinctItems: number;
  totalItems: number;
}

export function routeData() {
  return createServerData$<ScoreboardEntry[]>(async (_, { request }) => {
    const userId = await requireUserId(request);

    const raw = await sql`
        WITH scores AS (
            SELECT 
              user_id, 
              COUNT(inventory.item_id) as unique, 
              SUM(count * COALESCE(bid_price, 1)) as total 
            FROM inventory
            LEFT JOIN market ON market.item_id = inventory.item_id
            WHERE count > 0
            GROUP BY user_id
        )
        SELECT scores.user_id, users.username, scores.unique, scores.total
        FROM scores
        INNER JOIN users
        ON users.id = scores.user_id
        ORDER BY scores.unique DESC, scores.total DESC, scores.user_id ASC;
    `;

    return raw.map(({ username, unique, total }) => {
      return { username, distinctItems: Number(unique), totalItems: Number(total) };
    })
  });
}

export default function Scoreboard() {
  const data = useRouteData<typeof routeData>();
  return (
    <main>
      <div class="scoreboard">
        <div class="username">Username</div>
        <div class="unique">Unique</div>
        <div class="total">Total</div>
        <div class="sep"></div>
        <Suspense fallback={<p>Loading...</p>}>
          <Index each={data()}>
            {(item, index) => {
              return <>
                <div class="rank">{index + 1}</div>
                <div class="username">{item().username}</div>
                <div class="unique">{item().distinctItems}</div>
                <div class="total">{item().totalItems}</div>
              </>
            }}
          </Index>
        </Suspense>
      </div>
    </main >
  )
}