# Targeted 2026 literature-source verification (13 November 2026)

Primary publisher, preprint/archive, and official source URLs were checked as of November 2026. This is **not** an exhaustive systematic novelty review. The BibTeX in [references.bib](references.bib) uses these verified primary sources. Titles, full author lists and venue status should be checked again by the final corresponding author before submission.

| Research/technical source | Original publication | Verified use in manuscript |
|---|---|---|
| Jimenez et al., SWE-bench | [ICLR 2024 official proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html) | Software-issue and executable-test benchmark |
| Yu et al., SWE-ABS | [ICML 2026, PMLR 306:149974–150011](https://proceedings.mlr.press/v306/yu26b.html) | Adversarial test strengthening and shifting benchmark pass rates |
| Sahoo et al., AgentLens | [arXiv:2605.12925 (2026)](https://arxiv.org/abs/2605.12925) | Lucky-pass process-quality assessment and contextual actions |
| Shu et al., TraceProbe | [arXiv:2607.06184 (2026)](https://arxiv.org/abs/2607.06184) | Trajectory anti-patterns, difficulty association and process diagnostics |
| Guan et al., SWE-Cycle | [arXiv:2605.13139 (2026)](https://arxiv.org/abs/2605.13139) | Separate environment/implementation/verification stages and hybrid judge |
| Baltes et al., empirical LLM-SE guidelines | [Springer online 3 November 2026](https://link.springer.com/article/10.1007/s10664-026-10922-3) | Reproducibility, LLM roles, trace reporting and human validation |
| SWE-bench Verified original review | [OpenAI official 2024 release](https://openai.com/index/introducing-swe-bench-verified/) | Historical 500-instance human-reviewed subset; not SWE-ABS test review |
| SWE-bench Verified retrospective | [OpenAI official 23 February 2026 discussion](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) | General test-design and benchmark contamination concerns, NOT evidence of this study's actual model contamination |

## Source and novelty boundaries

- Named papers from the older synthetic paper's review are not automatically added if exact author/title/venue cannot be verified.
- SWE-ABS is peer-reviewed at ICML 2026; AgentLens, TraceProbe and SWE-Cycle are here cited by verified arXiv identifiers. Subsequent journal/conference publication status needs human checking.
- The online date for Baltes et al. is **2026**, while Springer labels volume 32 as **2027**; both should be made clear when citation formatting is finalized.
- Official vendor research posts are contextual evidence, **not** an independent peer-reviewed source or direct proof about the exact 198-run corpus.
- The narrow contribution is the specific exact-patch runner/trajectory join and documented sensitivity to label validity; do not claim invention of process features or of stronger testing.
- A comprehensive 2026 related-work sweep across ICSE, ASE, FSE, TOSEM, TSE, and EMSE remains **unverified** and is an explicit Step 13/mentor review gate.
