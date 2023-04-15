import { create } from "domain";
import { createEffect, createRenderEffect, createSignal, For, onCleanup, Show } from "solid-js";
import { FormError, useRouteData } from "solid-start";
import {
  createServerAction$,
  createServerData$,
  redirect,
} from "solid-start/server";
import sql from "~/db";
import { getUser, getUserSession, logout, requireUserId } from "~/db/session";
import * as fs from 'node:fs/promises';
import { requestHook } from "~/db/hook";
import { Form } from "solid-start/data/Form";
import toast from "solid-toast";

const COIN_ID = '0';

type MarketItem = {
  id: string,
  name: string,
  kind: string,
  bid_price: number | null,
  ask_price: number | null,
  bid_size: number | null,
  ask_size: number | null,
};

type RouteData = {
  userId: string,
  market: MarketItem[],
  inventory: { [item_id: string]: number },
  watchedItems: string[]
}

export function routeData() {
  return createServerData$<RouteData>(async (_, { request }) => {
    const userId = await requireUserId(request);


    const markets = await sql`
      SELECT kind, name, items.id, bid_price, bid_size, ask_price, ask_size FROM items
      LEFT JOIN market ON market.item_id = items.id
      ORDER BY items.id ASC
    `;

    const inventory = await sql`
      SELECT item_id, count FROM inventory
      WHERE user_id = ${userId}
        AND count > 0
    `;
    const inventoryDict = Object.fromEntries(inventory.map(x => [x.item_id, Number(x.count)]));

    const watching = await sql`
      SELECT DISTINCT kind FROM hooks
      WHERE user_id = ${userId}
    `;

    function stringnum(x: string | null): number | null {
      if (x) return Number(x);
      else return null;
    }

    const marketArray = markets.map(({ id, name, kind, bid_price, ask_price, bid_size, ask_size }) => {
      return {
        id,
        kind,
        name,
        bid_price: stringnum(bid_price),
        bid_size: stringnum(bid_size),
        ask_price: stringnum(ask_price),
        ask_size: stringnum(ask_size),
      }
    });

    return {
      userId,
      market: marketArray,
      inventory: inventoryDict,
      watchedItems: watching.map(x => x.kind)
    };
  });
}

export default function Home() {
  const data = useRouteData<typeof routeData>();
  const [, { Form: LogoutForm }] = createServerAction$((f: FormData, { request }) =>
    logout(request)
  );

  const [transacting, { Form: Transact }] = createServerAction$(async (f: FormData, { request }) => {
    const userId = await requireUserId(request);

    const action = f.get('action');

    if (action === 'buy' || action === 'sell') {
      const item = f.get('item');
      const size = f.get('size');
      if (typeof item !== 'string' || typeof size !== 'string') {
        throw new FormError('Bad submission');
      }

      const dirsign = action === 'buy' ? 1 : -1;
      const tradewith = action === 'buy' ? 'ask' : 'bid';
      const signedSize = dirsign * Number(size);

      try {
        await sql.begin(async (sql) => {
          await sql`
            INSERT INTO inventory (user_id, item_id, count)
            VALUES (${userId}, ${item}, 0)
            ON CONFLICT (user_id, item_id) DO NOTHING
          `;

          await sql`
          WITH current_market AS (
            UPDATE market
            SET ${sql(`${tradewith}_size`)} = ${sql(`${tradewith}_size`)} - ${size}
            WHERE item_id = ${item}
            RETURNING ${sql(`${tradewith}_price`)} as price
          )
          UPDATE inventory
          SET count = count - ${signedSize} * price
          FROM current_market
          WHERE item_id = ${COIN_ID} AND user_id = ${userId}
          `;

          await sql`
            UPDATE inventory
            SET count = count + ${signedSize}
            WHERE item_id = ${item} AND user_id = ${userId}
          `;
        });
      } catch (e) {
        throw new FormError(`You are no longer able to ${action} that item`);
      }

      return redirect('/');
    } else if (action === 'watch') {
      const target = f.get('url');
      const kind = f.get('kind');
      const secret = f.get('secret');
      if (typeof target !== 'string' || typeof kind !== 'string'
        || typeof secret !== 'string') {
        throw new FormError('Bad submission');
      }

      if (!/^[0-9]+$/.exec(secret)) {
        throw new FormError('Unable to start watching',
          { fieldErrors: { secret: 'Secret must be a number' } });
      }


      try {
        const newId = await sql`
          INSERT INTO hooks(user_id, kind, target, secret)
          VALUES (${userId}, ${kind}, ${target}, ${secret})
          RETURNING id
        `;

        return redirect(`/?watchId=${newId[0]!.id}`);
      } catch (e) {
        throw new FormError('Unable to watch that item')
      }
    } else if (action === 'unwatch') {
      const kind = f.get('kind');
      const hookId = f.get('id');

      if (typeof kind !== 'string' || (hookId && typeof hookId !== 'string')) {
        throw new FormError('Bad submission');
      }

      const hookFilter = hookId ? sql`id = ${hookId}` : sql`TRUE`;

      await sql`
        DELETE FROM hooks
        WHERE user_id = ${userId} AND kind = ${kind} AND ${hookFilter}
      `;

      return redirect('/');
    } else if (action === 'notify') {
      const kind = f.get('kind');
      if (typeof kind !== 'string') {
        throw new FormError('Bad submission');
      }

      if (await requestHook() !== 'can-hook')
        throw new FormError('Unable to notify at this time');

      const data = new URLSearchParams();
      data.append('kind', kind);
      for (const [key, value] of f.entries()) {
        if (typeof value !== 'string') throw new FormError('Bad submission');
        if (key === 'kind' || key === 'action') continue;
        data.append(key, value);
      }

      try {
        await fs.appendFile('/queue/hook', data.toString() + '\n');
      } catch (e) {
        throw new FormError('Unable to trigger the notification');
      }

      return redirect('/');
    } else {
      throw new FormError('Action is not implemented');
    }
  });

  const inventoryCount = (item_id: string) =>
    data()?.inventory?.[item_id] ?? 0;

  createEffect(() => {
    if (transacting.error) toast.error(transacting.error.message);
  });

  const notifyingItem = () =>
    transacting.input?.get('action') === 'notify';

  // TODO: progressively enhanced responses

  return (
    <main>
      <div class="markets">
        <For each={data()?.market}>
          {(it) => {
            const transactingHere = () =>
              transacting.input?.get('item') === it.id ? transacting : undefined;

            const transactingWatch = () =>
              (['watch', 'unwatch'] as unknown[]).includes(transactingHere()?.input?.get('action'));

            const [watchOverlayShown, showWatchOverlay] = createSignal(
              transactingWatch() && transactingHere()?.pending);

            const watchingItem = () => data()?.watchedItems.includes(it.kind);

            // hide or show the overlay based on whether we succeeded in watching
            createEffect(() => {
              if (transactingHere()?.pending === true && transactingWatch()) {
                onCleanup(() => {
                  if (!transactingHere()?.error) showWatchOverlay(false);
                });
              }
              if (transactingHere()?.pending === true && notifyingItem()) {
                onCleanup(() => {
                  if (!transactingHere()?.error) toast(`Notified watchers of ${it.name}`);
                });
              }
            });

            return <Transact>
              <div class="market">
                <input type="hidden" name="size" value="1" />
                <input type="hidden" name="item" value={it.id} />
                <input type="hidden" name="kind" value={it.kind} />
                <div class="image">
                  <img src={`items/${it.kind}.png`} />
                </div>
                <div class="item-name">
                  {it.name} ({inventoryCount(it.id)})
                </div>
                <div class="market-actions">
                  <button type="submit" name="action" value="buy" class="buy"
                    disabled={!(it.ask_price
                      && (it.ask_size ?? 0) > 0 && inventoryCount(COIN_ID) >= it.ask_price)}>
                    Buy {it.ask_price && `(${it.ask_price}g)`}
                  </button>
                  <button type="submit" name="action" value="sell" class="sell"
                    disabled={!(it.bid_price && (it.bid_size ?? 0) > 0
                      && inventoryCount(it.id) > 0)} >
                    Sell {it.bid_price && `(${it.bid_price}g)`}
                  </button>
                </div>
                <button class="notify-button" name="action" value="notify"
                  disabled={notifyingItem()}
                >⚡</button>
                <div class="watch-overlay" classList={{ shown: watchOverlayShown() }}>
                  <button class="watch-button"
                    onClick={() => showWatchOverlay(!watchOverlayShown())} type="button">{
                      watchingItem() ? '✅' : '👀'
                    }</button>
                  <Show when={watchOverlayShown()}>
                    <Show when={!watchingItem()}>
                      <input type="text" name="url" placeholder="URL" />
                      <Show when={transacting.error?.fieldErrors?.url}>
                        <p role="alert">{transacting.error.fieldErrors.url}</p>
                      </Show>
                      <input type="text" name="secret" placeholder="Secret" />
                      <Show when={transacting.error?.fieldErrors?.secret}>
                        <p role="alert">{transacting.error.fieldErrors.secret}</p>
                      </Show>
                      <button type="submit" name="action" value="watch">Watch</button>
                    </Show>
                    <Show when={watchingItem()}>
                      <button type="submit" name="action" value="unwatch">Stop watching</button>
                    </Show>
                  </Show>
                </div>
              </div>
            </Transact>
          }}
        </For>
      </div >

      <LogoutForm>
        <button name="logout" type="submit">
          Logout
        </button>
      </LogoutForm>
    </main >
  );
}
