# startup-idea-hunter-skill

Hunt, structure, and score startup, micro-SaaS, and AI product ideas using the **Easy-Vibe Stage 1** methodology (`appendix-idea-sources` + `finding-great-idea`).

Instead of guessing product features or building generic AI wrappers, this skill guides coding agents through:
1. **4-Channel Community & Market Clue Hunting**: Targeted search query packs across Reddit/forums, Capterra/G2 1-to-3 star reviews, Indie Hackers/Product Hunt launches, and Upwork/Fiverr repetitive jobs.
2. **Easy-Vibe Clue Page Structuring**: Preserves verbatim complaints, persona context, source links, and maps `Unstructured Input -> AI Capability -> Structured Output`.
3. **5-Criteria Startup Idea Scorecard & Need-Tier Classifier**: Evaluates `frequency` (20%), `pain_level` (25%), `current_workaround` (20%), `willingness_to_pay` (25%), and `market_size` (10%) with need-tier multipliers (`pain` 1.15x, `gratification` 1.0x, `desire` 0.75x).
4. **Value Reframing & 5-Step Validation Plan**: Narrows broad ideas horizontally, maps the vertical context timeline, and outputs a concrete 10-user + >10% pre-order validation plan.

## Installation

### Universal Path (works with 6+ tools)

```bash
git clone https://github.com/aidino/startup-idea-hunter-skill.git ~/.agents/skills/startup-idea-hunter-skill
```

Works with Codex CLI, Gemini CLI, Kiro, OpenCode, Goose, Antigravity, and other tools that read `~/.agents/skills/`.

### Claude Code (plugin — recommended)

```
/plugin marketplace add aidino/startup-idea-hunter-skill
/plugin install startup-idea-hunter-skill@startup-idea-hunter-skill
```

### Using install.sh (Recommended for all 17 platforms)

```bash
chmod +x install.sh
./install.sh                          # Auto-detect platform
./install.sh --platform claude-code   # Claude Code
./install.sh --platform cursor        # Cursor (auto-generates .mdc)
./install.sh --all                    # All detected platforms
./install.sh --dry-run                # Preview without installing
```

### Alternative: npx

```bash
npx skills add https://github.com/aidino/startup-idea-hunter-skill
```

### Manual Installation

| Platform | Copy to |
|---|---|
| Universal | `~/.agents/skills/startup-idea-hunter-skill/` |
| Claude Code | `~/.claude/skills/startup-idea-hunter-skill/` |
| GitHub Copilot | `.github/skills/startup-idea-hunter-skill/` |
| Cursor | `.cursor/rules/startup-idea-hunter-skill/` |
| Windsurf | `.windsurf/rules/startup-idea-hunter-skill/` |
| Cline | `.clinerules/startup-idea-hunter-skill/` |
| Codex CLI | `~/.agents/skills/startup-idea-hunter-skill/` |
| Gemini CLI | `~/.gemini/skills/startup-idea-hunter-skill/` |
| Kiro | `.kiro/skills/startup-idea-hunter-skill/` |
| Trae | `.trae/rules/startup-idea-hunter-skill/` |
| Goose | `~/.config/goose/skills/startup-idea-hunter-skill/` |
| OpenCode | `~/.config/opencode/skills/startup-idea-hunter-skill/` |
| Roo Code | `.roo/rules/startup-idea-hunter-skill/` |
| Antigravity | `~/.agents/skills/startup-idea-hunter-skill/` |

## Prerequisites

- Python 3.9+ (uses standard library only; no third-party pip packages required).

```bash
python3 scripts/run_pipeline.py --check-prereqs
```

## How to Use in Your Coding Agent (Cách sử dụng)

Sau khi cài đặt, bạn **không cần tự chạy script Python bằng tay**. Hãy gọi trực tiếp skill trong khung chat của Coding Agent (Claude Code, Cursor, Codex, GitHub Copilot, OpenCode, Gemini CLI...) bằng lệnh `/startup-idea-hunter-skill` hoặc ngôn ngữ tự nhiên:

### 1. Truy lùng ý tưởng từ đầu theo một ngách (Chưa có manh mối sẵn)
Gõ vào Coding Agent:

```text
/startup-idea-hunter-skill Hãy giúp tôi truy lùng manh mối và tìm ý tưởng AI startup trong lĩnh vực công việc tự do (freelancing), có ghi nguồn rõ ràng.
```
*(Hoặc tiếng Anh)*:
```text
/startup-idea-hunter-skill Hunt AI micro-SaaS startup ideas in the property management niche using the 4-step Easy-Vibe workflow.
```

**Agent sẽ tự động thực hiện:**
1. Sinh bộ câu lệnh tìm kiếm trên **4 kênh** (Reddit/cộng đồng, review 1–3 sao trên Capterra/G2, Indie Hackers/Product Hunt, và chợ việc làm lặp lại trên Upwork/Fiverr).
2. Dùng công cụ tìm kiếm (Web Search) của Agent để thu thập lời phàn nàn nguyên văn (verbatim quotes), bối cảnh người dùng và link nguồn.
3. Ánh xạ từng vấn đề sang luồng dữ liệu **Input $\rightarrow$ AI Capability $\rightarrow$ Output**.
4. Chấm điểm theo **5 tiêu chí Easy-Vibe** (`Frequency`, `Pain Level`, `Current Workaround`, `Willingness to Pay`, `Market Size`), phân tầng nhu cầu (`pain` > `gratification` > `desire`) và xuất ra **Trang Manh Mối + Kế hoạch 5 bước kiểm chứng MVP**.

---

### 2. Chấm điểm & Sàng lọc các ghi chú / ý tưởng bạn đã gom được
Khi bạn đã có sẵn một vài phàn nàn của người dùng, link bài viết hoặc file ghi chú:

```text
/startup-idea-hunter-skill Tôi vừa gom được 4 vấn đề từ Reddit và Upwork trong file clues.json. Hãy chấm điểm theo chuẩn Easy-Vibe xem ý tưởng nào là nỗi đau thật (painkiller) đáng làm MVP nhất và loại bỏ các ý tưởng vitamin.
```

---

### 3. Tái cấu trúc (Reframe) một ý tưởng chung chung thành ngách có người trả tiền
Nếu bạn đang có một ý tưởng còn rộng (ví dụ: *"Làm app quản lý chi tiêu bằng AI"* hoặc *"Làm app tập thể dục"*):

```text
/startup-idea-hunter-skill Tôi muốn làm ứng dụng AI ghi chú cuộc họp. Hãy dùng phương pháp chia ngang nhóm người dùng (horizontal segmentation) và đào sâu bối cảnh (vertical timeline) của Easy-Vibe để tìm ra ngách hẹp có khả năng chi trả cao nhất.
```

---

### 4. Dạy lại Skill khi bạn muốn tinh chỉnh kết quả (`--correct`)
Nếu bạn muốn chỉnh lại cách skill đánh giá trong những lần chạy sau, hãy bảo Agent:

```text
Hãy ghi nhận hiệu chỉnh cho startup-idea-hunter-skill: "Ưu tiên các bài toán B2B xử lý chứng từ PDF/Excel hơn là công cụ B2C"
```
*(Agent sẽ tự chạy `scripts/evolve.py --correct` để cập nhật bộ nhớ `## Gotchas` và tạo bài test chống hồi quy).*

---

## Under the Hood (CLI dành cho Agent & CI)

Bên dưới lớp giao tiếp tự nhiên, Coding Agent sẽ tự động gọi các script định sẵn trong `scripts/` để đảm bảo tính toán điểm số nhất quán:

```bash
# Agent chạy pipeline chấm điểm & xuất báo cáo Markdown + JSON:
python3 scripts/run_pipeline.py \
  --input evals/golden/case-1/input.json \
  --output output/freelance-scorecard.json \
  --markdown output/freelance-scorecard.md

# Agent sinh bộ query săn manh mối 4 kênh:
python3 scripts/generate_queries.py --niche "property management" --output output/queries.json

# Kiểm tra Evals & Bảo trì định kỳ:
python3 scripts/run_evals.py --validate
python3 scripts/run_evals.py --rollout
python3 scripts/evolve.py
```

## Verification

See [VERIFICATION.md](VERIFICATION.md) for recorded gate results and rollout evidence.
