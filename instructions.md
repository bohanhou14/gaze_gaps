**Task Overview**

You are tasked to classify categories of gaps between machine-generated and human-written legal analysis. 

**Definitions**

**generation**: machine-generated legal analysis.

**target**: human-written legal analysis. Note that the target is only one form of acceptable legal analysis. There are other acceptable legal analysis. It is possible for a generation to not match with the target but still considered acceptable.

**previous_context**: we set the goal of LLM to generate a paragraph of legal analysis and feed in the previous context to this paragraph as the input.

**cited_paragraphs**: in addition to the previous context, we also feed in the other paragraphs that are supposed to be cited in this generation.

**citation**: citation refers to the special string which points to a legal case, with style and format specified by the Bluebook.

**claim**: the sentence which is supported by the citation, i.e. the case referred to. Claim usually appears in the vicinity of the citation.

**Intrinsic Gaps**: the presence of instrinsic gaps signals that the machine-generated legal analysis is an unacceptable form. We can tell instrinsic gaps exist by _only_ looking at the previous context and the generation itself.

**Extrinsic Gaps**: extrinsic gaps, as its name suggests, can be discovered by comparing the generation with external texts, i.e. the cited paragraphs or the target paragraph that can be seen as the "answer". Extrinsic gaps contain two kinds: citation content mismatch and target mismatch. Target mismatch does not indicate that the generated legal analysis is necessarily wrong.

**Gaps Categories**

**Intrinsic gaps**:

* ***Redundancy*** (1): the generation appears to make repetitive statements that do not add more meaning to the analysis.

* ***Citation Format Mismatch*** (2): the generation appears not matching with the citation format of the standard Bluebook.

* ***Structural Mismatch*** (3): the generation appears to generate the document from scratch (like containing words such as "ORDER" which only appear in the beginning).

* ***Stylistic Mismatch*** (10): contain sentences that do not match the styles of legalese.



**Extrinsic Gaps**

* Citation Content Mismatch: 

    * Claim Hallucination (4): the claim supported by the citation is not truthful or not related to the context or from cited paragraphs or the previous context.

    * Retrieval Inaccuracy (5): the claims supported by the citation is not relevant because the cited paragraph looks irrelevant compared to the target paragraph. If retrieval inaccuracy is labeled, there is no need to label claim hallucination.

    * Citation Hallucination (6): the citation is non-existent or pulled from a citation in the cited paragraphs or the previous context, or there misses a citation.

* Target Mismatch

    * Relation Mismatch: 

        * Chain Cite (7): the citations appear in a chain cite but the generation cites them parallely, or the other way around.

        * Reverse Cite (8): the citations reverse the ruling in each other but the generation cites them parallely, or the other way around.

        * Compound Cite (9): the citations of different cases are cited together, separated by semicolons, or the other way around.

* No gaps (0)

* Other/Undefined (11)

**Instructions to Annotators**

Note that an example may have several categories of gaps, so annotate each example as many as possible.

Please annotate the most specific name of the error after "Label: ". For example, "Compound Cite" instead of "Relation Match".

