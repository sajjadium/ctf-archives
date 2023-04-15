import { Map } from "immutable";

export async function asyncBindMap<K, V1, V2>(
	map: Map<K, V1>,
	fn: (value: V1, key: K) => Promise<V2>
): Promise<Map<K, V2>> {
	const entries = map.entrySeq().toArray();
	const newEntries = await Promise.all(
		entries.map(async ([key, value]): Promise<[K, V2]> => {
			const newValue = await fn(value, key);
			return [key, newValue];
		})
	);
	return Map(newEntries);
}
