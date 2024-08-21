*Instructions to Annotators*

You are tasked to classify categories of gaps between machine-generated and human-written legal analysis. 

*Definitions*
**generation**: Machine-generated legal analysis.

**target**: Human-written legal analysis. Note that the target is only one form of acceptable legal analysis. There are other acceptable legal analysis. It is possible for a generation to not match with the target but still considered acceptable.

**previous_context**: We set the goal of LLM to generate a paragraph of legal analysis and feed in the previous context to this paragraph as the input.

**cited_paragraphs**: In addition to the previous context, we also feed in the other paragraphs that are supposed to be cited in this generation.

**Intrinsic Gaps**: The presence of instrinsic gaps signals that the machine-generated legal analysis is an unacceptable form. We can tell instrinsic gaps exist by _only_ looking at the previous context and the generation itself.

**Extrinsic Gaps**: Extrinsic gaps, as its name suggests, can be discovered by comparing the generation with external texts, i.e. the cited paragraphs or the target paragraph that can be seen as the "answer". Extrinsic gaps contain two kinds: citation content mismatch and target mismatch. Target mismatch does not indicate that the generated legal analysis is necessarily wrong.

*Gaps Categories*

**Intrinsic gaps**:

***Redundancy***: the generation appears to make repetitive statements that do not add more meaning to the analysis.

***Stylistic Mismatch***: the generation appears not matching with the citation style of the standard Bluebook.

***Structural Mismatch***: the generation appears

