// Loads data.json + tech_tree.json + builder_slots.json + game_settings.json.
// Editor lives at repo-root/editor/. data.json and derived/ both sit at the
// repo root (since 2026-05-01).

export async function loadAll() {
  const [data, tree, slotsRaw, settings] = await Promise.all([
    fetch("../data.json").then(r => r.json()),
    fetch("../derived/tech_tree.json").then(r => r.json()),
    fetch("../derived/builder_slots.json").then(r => r.json()),
    fetch("../derived/game_settings.json").then(r => r.json()),
  ]);
  const slots = {};
  for (const [sid, info] of Object.entries(slotsRaw)) {
    slots[sid] = info.slots;
  }
  return { data, tree, slots, settings };
}
