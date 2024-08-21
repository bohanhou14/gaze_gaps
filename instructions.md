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

**Annotation Instructions**
In the following order, you should consider:
1. The relationship between the generated text and the previous context.
2. The relationship between the generated text and the target text
3. The relationship between the generated text and the citations that it points to.

This will entail labeling for:

1. Intrinsic error/LLM error: The language model has fundamentally failed to follow the instruction. Some causes might be that
    - it repeats itself several times
    - it responds as if in a chat environment
    - it contradicts something from earlier in the context
    - the generated text does not look like legal text

    or simply that the text it generates does not seem like a plausible continuation of the immediately preceding context. If this type of error is **present**, add the label `1` and move on to the next example. If it is **not present**, continue to item (2).

1. Target Mismatch: The language model's generated text may not be obviously wrong, but it makes substantively different claims from the target text (i.e. the original text from the case). This could be because
    - the citations are grouped in a different way from the target
    - the generated text makes different and possibly (although not necessarily) contradictory claims about one or more citations from those made in the target text

    If this type of mismatch is **present** add the label `2` and continue to item (3). If it is **not present**, add the label `0` and move on to the next example.

3. Citation Error: The language model's generated text does not align with the content of the citation it points to. This might be because
   - the generated text attributes information from one citation to a different citation
   - the generated text fails to use one of the citations that were given to it
   - one of the retrieved contains no relevant information about the case

    If this type of error is **present**, add the label `3` and move on to the next example.

Note that where an example falls into multiple categories (typically both 2 and 3), you should include both labels, separated by a comma.