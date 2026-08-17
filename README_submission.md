# Lab 17 Submission

## Phan tich

Trong bo test nay, long-term memory quan trong nhat vi phu bon case E02, E03, E08, E09 va dong gop vao E07. No phai nho preference qua session, open loop, tach user va xu ly preference moi theo scope. Episodic va semantic it case hon nhung van bat buoc de recall trajectory va domain rule.

Baseline no-memory dat 2/11 (18,18%): chi E01 va E10 short-term pass; long-term, episodic, semantic va mixed deu 0%. Student retrieval dat 11/11 (100%); practice moi layer deu pass, nen khong co layer yeu nhat trong bo test nay. E03 retrieve nhieu token nhat (1.804 token), tiep theo E08 (1.782). E07 la mixed long-term + semantic va bat buoc co ca `Python` va `Idempotency-Key`.

No-memory co token reduction trung binh 81,82% vi hau het case tra context rong. Day khong phai toi uu tot: reduction chi co y nghia khi di cung evidence hit rate. Memory-enabled chap nhan them token de dua dung evidence vao context, sau do budget 10/4/3/3 cat phan du thua.

E08 minh hoa recency theo scope: `BLUEBIRD-42` dung TypeScript/NestJS, trong khi Python van hop le cho demo ca nhan `ORCHID-27`; khong nen xoa fact cu khoi scope khac. E10 cho thay compaction phai giu durable constraint `REVIEW-DEADLINE-1600`, Friday 16:00 ngay ca khi raw turn da bi evict. Golden dat 20/20, bonus 10/10. Buffer don thuan tang token tuyen tinh va khong tao durable note.

## Trade-off va guardrail

Zep Context Block tu dong lap rap user context, graph facts, recency va provenance, giam code orchestration. Redis + Qdrant cho quyen kiem soat schema, TTL, chi phi va ha tang, nhung phai tu xay extraction, namespace, conflict resolution, ranking, deletion va observability.

De chong memory poisoning, durable write can opt-in, user-scoped namespace, allowlist type, source/timestamp/confidence, PII minimization va review cho preference/task tac dong cao. Retrieval uu tien fact moi dung scope, van giu provenance cua fact bi supersede. Heartbeat chi duoc deduplicate/expire/recap, khong tu cap quyen hay tao instruction moi. Privacy drill xac nhan Zep user da bi xoa va Redis con 0 user key.
