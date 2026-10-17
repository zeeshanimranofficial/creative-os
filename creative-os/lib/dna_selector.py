"""Creative OS v2 — DNA Selector (M5).

Picks exactly ONE active DNA profile for a brief. Never invents, never
hybridizes. Scoring is transparent (logged per candidate). If confidence
is below threshold, the OS does NOT generate: it returns the nearest
candidates for human approval (locked decision: missing DNA -> suggest
nearest + approval BEFORE generating).
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRESHOLD = 6  # below this best-score, require human approval

# post-type keywords -> collection boosts
TYPE_HINTS = {
    "before_after": ["before", "after", "transformation", "results", "glow", "improve"],
    "infographics": ["infographic", "stats", "data", "steps", "process", "factors", "listicle", "numbers"],
    "infographics_extended": ["infographic", "stats", "data", "steps", "process", "factors", "wheel", "timeline"],
    "occasions_eid_islamic": ["eid", "ramadan", "islamic", "qurbani", "mubarak"],
    "occasions_national_days": ["independence", "labour", "national", "tribute", "day"],
    "occasions_fun_days": ["chocolate day", "fun day", "pun", "meme", "humor"],
    "occasions_month_transition": ["new month", "month transition"],
    "announcements_teasers": ["announcement", "teaser", "coming soon", "reveal"],
    "announcements_extended": ["save the date", "countdown", "anniversary", "milestone", "launch", "city"],
    "community_giveaway": ["winner", "giveaway", "contest"],
    "mockup_scenes": ["mockup", "post mockup", "services"],
    "mockup_scenes_extended": ["trust", "website", "device"],
    "hero_objects": ["idea", "growth", "stand out"],
    "hero_objects_extended": ["delivery", "on time", "clock"],
    "listicle_cards": ["myth", "fact", "misconception"],
}


def _text_of(e):
    parts = [e.get("collection", ""), e.get("working_label", ""), e.get("name", ""),
             e.get("composition_dna", ""), " ".join(e.get("archetype_tags", []))]
    c = e.get("constraints", {})
    parts += c.get("locked", []) + c.get("flexible", [])
    return " ".join(str(p) for p in parts).lower()


def _tokens(s):
    return set(re.findall(r"[a-z]{3,}", s.lower()))


def select(registry, brief, top_n=3):
    """brief: {topic, post_type_hint?, platform?}. Returns dict:
    {decision: 'auto'|'needs_approval', chosen?, candidates: [(id, score, why)]}"""
    q = (brief.get("post_type_hint", "") + " " + brief["topic"]).lower()
    qtok = _tokens(q)
    scored = []
    for e in registry["entries"]:
        if e.get("status") == "purged":
            continue
        eid = e.get("id", e.get("registry_id"))
        txt = _text_of(e)
        score, why = 0, []
        # keyword overlap
        ov = qtok & _tokens(txt)
        score += min(len(ov), 8)
        if ov:
            why.append("keywords:" + ",".join(sorted(ov)[:5]))
        # type-hint collection boost
        for coll, kws in TYPE_HINTS.items():
            if e.get("collection") == coll and any(k in q for k in kws):
                score += 6
                why.append(f"type-hint:{coll}")
                break
        scored.append((score, eid, "; ".join(why) or "no signal"))
    scored.sort(reverse=True)
    cands = [{"id": i, "score": s, "why": w} for s, i, w in scored[:top_n]]
    if scored and scored[0][0] >= THRESHOLD:
        return {"decision": "auto", "chosen": cands[0]["id"], "candidates": cands}
    return {"decision": "needs_approval",
            "message": "No confident DNA match — per locked policy the OS will NOT generate. "
                       "Nearest profiles listed; a human must approve one (or add a new reference via intake).",
            "candidates": cands}
