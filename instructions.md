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

* ***Redundancy***: the generation appears to make repetitive statements that do not add more meaning to the analysis.

* ***Citation Format Mismatch***: the generation appears not matching with the citation format of the standard Bluebook.

* ***Structural Mismatch***: the generation appears to generate the document from scratch (like containing words such as "ORDER" which only appear in the beginning).

* ***Misattribution***: the generation appears to use citation from the previous contexts instead of citations that it is supposed to use.



**Extrinsic Gaps**

* Citation Content Mismatch: 

    * Claim Hallucination: the claim supported by the citation is not truthful or not related to the context.

    * Retrieval Inaccuracy: the claims supported by the citation is not relevant because the cited paragraph looks irrelevant compared to the target paragraph. If retrieval inaccuracy is labeled, there is no need to label claim hallucination.

    * Citation Hallucination: the citation is non-existent or pulled from a citation in the cited paragraphs.

    * Entity Hallucination: the entities associated with the citations are not truthful or are non-existent.

* Target Mismatch

    * Relation Mismatch: 

        * Chain Cite: the citations appear in a chain cite but the generation cites them parallely, or the other way around.

        * Reverse Cite: the citations reverse the ruling in each other but the generation cites them parallely, or the other way around.

        * Compound Cite: the citations of different cases are cited together, separated by semicolons, or the other way around.

    * Citation Style Mismatch: the citations are cited in a different style in the target than the generation. Examples include citations should be cited together, separated by semicolons, but the generation elaborates each one with a claim from the case referred to.

**Instructions to Annotators**
Note that an example may have several categories of gaps, so annotate each example as many as possible.

Please annotate the most specific name of the error after "Label: ". For example, "Compound Cite" instead of "Relation Match".

