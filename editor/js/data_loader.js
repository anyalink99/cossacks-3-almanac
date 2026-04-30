// Loads data.json + tech_tree.json + builder_slots.json + game_settings.json.
// Editor lives at repo-root/editor/, so docs/ is one level up.

export async function loadAll() {
  const [data, tree, slotsRaw, settings] = await Promise.all([
    fetch("../docs/data.json").then(r => r.json()),
    fetch("../docs/derived/tech_tree.json").then(r => r.json()),
    fetch("../docs/derived/builder_slots.json").then(r => r.json()),
    fetch("../docs/derived/game_settings.json").then(r => r.json()),
  ]);
  const slots = {};
  for (const [sid, info] of Object.entries(slotsRaw)) {
    slots[sid] = info.slots;
  }
  return { data, tree, slots, settings };
}
