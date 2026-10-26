# Evaluation Specification: `startup-idea-hunter-skill`

This specification defines the binary quality criteria and golden cases for `startup-idea-hunter-skill`.

## Binary Criteria

1. **`valid-json-structure`**: Output is valid JSON containing `niche`, `query_pack`, `summary`, `ranked_clues`, and `mvp_validation_plan`.
2. **`four-channel-query-pack`**: `query_pack.channels` contains all 4 Easy-Vibe hunting channels (`reddit_community_pain`, `capterra_low_star_reviews`, `indie_hackers_product_hunt`, `upwork_fiverr_repetitive_jobs`), each with at least 3 search queries.
3. **`clue-page-evidence-preserved`**: Every entry in `ranked_clues` preserves a non-empty verbatim `quote`, `persona_context`, `input_data`, `output_data`, `ai_capability`, and `source_url`.
4. **`scorecard-sorted-and-bounded`**: `ranked_clues` are sorted in descending order by `adjusted_score_100` (all in `[0, 100]`), and any clue with `need_tier == "desire"` is penalized (`need_tier_multiplier == 0.75`) and never given a `"BUILD_MVP_NOW"` verdict.
5. **`five-step-mvp-validation-plan`**: `mvp_validation_plan` targets the #1 ranked clue (`winning_clue_id == ranked_clues[0].id`) and includes all 5 Easy-Vibe demand validation steps.

```json
{
  "skill": "startup-idea-hunter-skill",
  "run": "python3 scripts/run_pipeline.py --input {input} --output {output}",
  "criteria": [
    {
      "id": "valid-json-structure",
      "text": "Output is valid JSON containing niche, query_pack, summary, ranked_clues, and mvp_validation_plan",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert all(k in d for k in (\"niche\",\"query_pack\",\"summary\",\"ranked_clues\",\"mvp_validation_plan\"))' {output}"
    },
    {
      "id": "four-channel-query-pack",
      "text": "query_pack contains all 4 Easy-Vibe hunting channels with at least 3 search queries each",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); ch=d[\"query_pack\"][\"channels\"]; assert len(ch)==4 and all(len(c[\"queries\"])>=3 for c in ch)' {output}"
    },
    {
      "id": "clue-page-evidence-preserved",
      "text": "Every ranked clue preserves verbatim quote, persona_context, input_data, output_data, ai_capability, and source_url",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); rc=d[\"ranked_clues\"]; assert len(rc)>=2 and all(all(bool(c.get(f)) for f in (\"quote\",\"persona_context\",\"input_data\",\"output_data\",\"ai_capability\",\"source_url\")) for c in rc)' {output}"
    },
    {
      "id": "scorecard-sorted-and-bounded",
      "text": "Clues are sorted descending by adjusted_score_100 in [0,100] and desire-tier clues never receive BUILD_MVP_NOW",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); rc=d[\"ranked_clues\"]; scores=[c[\"adjusted_score_100\"] for c in rc]; assert scores==sorted(scores,reverse=True) and all(0<=s<=100 for s in scores) and all(c[\"verdict\"]!=\"BUILD_MVP_NOW\" for c in rc if c[\"need_tier\"]==\"desire\")' {output}"
    },
    {
      "id": "five-step-mvp-validation-plan",
      "text": "mvp_validation_plan matches the top-ranked clue and includes all 5 Easy-Vibe demand validation steps",
      "type": "command",
      "cmd": "python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); p=d[\"mvp_validation_plan\"]; assert p[\"winning_clue_id\"]==d[\"ranked_clues\"][0][\"id\"] and len(p[\"five_step_validation\"])==5' {output}"
    }
  ],
  "golden": [
    {
      "id": "case-1",
      "input": "golden/case-1/input.json",
      "expected": "golden/case-1/expected.json",
      "split": "val"
    },
    {
      "id": "case-2",
      "input": "golden/case-2/input.json",
      "expected": null,
      "split": "test",
      "expected_status": "pending-first-green"
    },
    {
      "id": "case-3",
      "input": "golden/case-3/input.json",
      "expected": null,
      "split": "val",
      "expected_status": "pending-first-green"
    }
  ]
}
```
