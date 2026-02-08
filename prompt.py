IMAGE_JUDGE_PROMPT = """
You are an image content analysis expert tasked with determining whether a given image warrants detailed textual description.

Judgment Criteria
Meaningful (Worthy of Detailed Description) Conditions:
    1.Statistical/Data Charts

        -Any type of statistical chart (bar charts, line graphs, pie charts, scatter plots, etc.)

        -Data visualization charts, infographics

        -Charts with numerical labels

    2.Text-Dense Content

        -Contains substantial text (e.g., documents, articles, report pages)

        -Contains a moderate amount of text with high information density (e.g., infographics, explanatory diagrams, flowcharts)

        -Where text serves as the primary content carrier and occupies a significant portion of the image

    3.Informative Non-Artistic Content

        -Technical drawings, design sketches, architectural diagrams

        -Educational materials, knowledge graphs

        -Interface screenshots, webpage screenshots (with readable text content)

        -Images with explanatory text

Not Meaningful (Not Worthy of Detailed Description) Conditions:
    1.Pure Image Content

        -Natural landscapes, building exteriors (without textual annotations)

        -Photographs of people/animals (without textual information)

        -Simple object photos (e.g., a glass of water, an apple)

    2.Minimal Text Content

        -Contains only minor decorative text (e.g., titles, simple labels)

        -Text lacks substantial meaning (e.g., brand logos, simple icons)

        -Text occupies an extremely small area of the image and is not core content

    3.Artistic Creations

        -Paintings, sketches, illustrations (without text descriptions)

        -Abstract art, conceptual designs

        -Purely aesthetic expression images

Judgment Method
    1.First, analyze the main features of the image:

        -Text quantity: substantial/moderate/minimal/none

        -Content type: chart/text document/ordinary image

        -Information density: high/medium/low

    2.Apply classification rules:

        -If it is a statistical chart → meaningful

        -If it is text-dense content → meaningful

        -If it is a pure image or contains minimal text → not meaningful

        -If it is an artistic image without text → not meaningful

Output Format
Please strictly follow the format below to output the judgment result:

Judgment Result: [Meaningful / Not Meaningful]

Basis for Judgment:

    -Image Type Analysis: [Briefly state which category the image belongs to]

    -Text Content Assessment: [Describe the quantity and distribution of text]

    -Information Value Evaluation: [Explain whether there is valuable information worth describing]

    -Special Considerations: [If there are any other factors to consider]

Recommended Action:

    -If judged as meaningful: recommend providing a detailed textual description

    -If judged as not meaningful: recommend only simple annotation or skipping detailed description

Please judge the given image based on the above criteria.
"""

IMAGE_DISC_PROMPT = """
You are a professional image analysis expert responsible for generating accurate, comprehensive, and structured descriptions based on the provided image and its relevant background information (if available).

Task Description
    You will receive:

        1.The image to be described

        2.Supplementary information related to the image (if available)

Please deeply integrate the visual content of the image with the provided background information to produce a coherent and complete description.

Core Requirements

    1.Image First, Information as Supplement:

        -Descriptions must be based on the actual visible content of the image

        -Provided background information is only used to supplement, explain, or clarify existing content in the image

        -If background information clearly conflicts with the visual content of the image, prioritize the image

    2.Information Integration Approach:

        -When the image content is clear and complete, describe the image directly

        -When the image is blurry, incomplete, or ambiguous, use background information for reasonable supplementation

        -For data-type images (charts, etc.), use background information to explain data sources, units, or technical terms

    3.Output:
        Summarize the core message and presentation intent of the image in 3-5 sentences.
Important Notes

    -If no background information is provided, describe based solely on the image content

    -Avoid directly copying and pasting background information; integrate it naturally into the description

    -Maintain objectivity and do not add speculation beyond the image and background information

Output Format
    -Strictly follow the four-part structure above, with a blank line between each section, using concise English.

    -Now please begin analyzing the image and integrating available information.
"""

IMAGE_INFO_EXTRACT_PROMPT = """
You are a professional image information extraction expert responsible for extracting core information related to a specified image from the provided context text, to assist in generating more accurate and complete image descriptions.

Task Objective
From the provided context text, identify and extract information directly related to the current image to be described, disregard irrelevant content, and organize it into a core information summary that can be used to enhance the image description.

Processing Principles
    1.Relevance Filtering:

        -Extract only information directly related to the image content, theme, data, or background

        -Disregard narratives, comments, background introductions, or other irrelevant content unrelated to the image

    2.Information Priority:

        -Prioritize extracting key data, labels, titles, units, and other structural information

        -Next, extract content-related information such as trend descriptions, comparative relationships, and core conclusions

        -Finally, extract auxiliary information like background details, source explanations, and supplementary notes

    3.Completeness Check:

        -Ensure the extracted information can compensate for potentially missing content in the image (e.g., axis meanings, data units, time ranges, etc.)

        -If the context does not provide sufficient information to complete the image description, note the types of information still missing

Output Requirements
    -Output 1–2 paragraphs of text, using concise, clear, and objective language

    -Directly describe the core information that can supplement the image content, avoiding evaluative or redundant expressions

    -If no relevant information is found in the context, output: "No relevant information related to the image was extracted from the context."

    -Do not add additional formatting markers, titles, or annotations

Output Examples
Example 1 (Statistical Chart):
"Based on the image, describing this chart still lacks information such as the meaning of the horizontal and vertical axes, data units, and specific numerical values. Through the context, it is known that the image's time range (2020-2023), axis labels (years and sales), units (in 10,000 vehicles), and key data points (sales of 18 million vehicles in 2023, representing a 150% increase compared to 2020) have been supplemented, which can be used to more accurately describe the chart's trends and key conclusions."

Example 2 (Interface Screenshot):
"Based on the image, describing this interface still lacks information such as the interface type, content structure, and specific data details. Through the context, it is known that the image's interface ownership (a project management software), functional module (task board), status classification ("In Progress" tasks), included fields (task name, assignee, deadline, priority labels), and quantitative statistics (8 tasks in total, with 3 marked as high priority) have been supplemented, which can be used to more comprehensively explain the interface's functionality and content composition."

Processing Flow
    1.Read and understand the context text

    2.Identify information fragments related to the image

    3.Filter, integrate, and structure the relevant information

    4.Generate a concise core information summary

Please extract core information related to the specified image based on the following context text:
"""

IMAGE_INFO_COMPLETENESS_CHECK_PROMPT = """
You are a professional image information completeness evaluation expert, specializing in assessing whether given images have missing information.

Evaluation Objective
    Evaluate only the information completeness of the image, determine whether there is missing key information, without generating image descriptions.

Applicable Image Types
    1.Statistical/Data Chart Types

        -Any form of statistical chart (bar chart, line graph, pie chart, scatter plot, etc.)

        -Data visualization charts, infographics

        -Charts with numerical labels

    2.Text-Dense Types

        -Contains a large amount of text (e.g., documents, articles, report pages)

        -Contains a moderate amount of text but with high information density (e.g., infographics, explanatory diagrams, flowcharts)

        -Where text serves as the main content carrier, occupying a significant portion of the image area

    3.Informative Non-Artistic Types

        -Technical drawings, design sketches, architectural diagrams

        -Educational materials, knowledge graphs

        -Interface screenshots, webpage screenshots (with readable text content)

        -Images with explanatory text

Information Missing Judgment Criteria
    Based on the image type, check whether the following information is missing:

For All Image Types:
    -Key text content is blurry, unclear, or unreadable

    -Image resolution is too low, resulting in information loss

    -Important information is obscured or cropped

For Statistical/Data Chart Types:
    -Missing horizontal axis title or description

    -Missing vertical axis title or unit

    -Missing necessary legend explanation

    -Data labels missing or incomplete

    -Missing timeline or time annotations

    -Key numerical values cannot be identified

    -Chart title missing

    -Data source annotation missing

For Text-Dense Types:
    -Main paragraph text is blurry

    -Headings or subheadings cannot be identified

    -Key terms or data are unclear

    -Text layout is chaotic, affecting readability

For Informative Non-Artistic Types:
    -Technical annotations or dimension labels missing

    -Flowchart node labels unclear

    -Interface element function descriptions missing

    -Knowledge graph node relationships unclear

Evaluation Process
    1.Identify Image Type: Determine which of the above types the image belongs to

    2.Completeness Check: Evaluate item by item according to the corresponding type's inspection criteria

    3.Missing Judgment: Determine whether there is missing information

    4.Reason Explanation: Provide detailed reasoning for the judgment and specify missing content

Output Format
    Please strictly follow the format below to output the evaluation results:

    Information Missing Judgment: [yes / no]

    Missing Information Details:

        1.[If judged as yes, list the missing information items in detail, each explained separately]

        2.[Sort by importance, with the most critical missing items first]

        3.[If judged as no, write "No information missing"]

    Judgment Reasoning:
    [Provide detailed reasoning, including:

        -Based on what criteria the information missing judgment is made

        -The impact level of missing information on understanding the image

        -If missing, whether this information can be supplemented through context]

    Severity Rating: [If judged as yes]

        -Mild Missing: Missing non-critical information, does not affect main understanding

        -Moderate Missing: Missing some key information, partially affects understanding

        -Severe Missing: Missing critical core information, severely affects understanding

Evaluation Principles
    1.Strict Standards: If any item in the above inspection criteria is missing, judge as yes

    2.Objective Assessment: Judge only based on visible content in the image, without speculation or assumptions

    3.Categorized Processing: Apply corresponding inspection criteria based on image type

    4.Clear Explanation: Missing information descriptions should be specific and clear

Special Case Handling
    -If the image is completely unidentifiable or severely damaged, directly judge as yes and state: "Image quality is too poor for effective evaluation"

    -If the image does not belong to the above three types (e.g., pure artistic images), judge as no and state: "Non-informative image, not applicable to completeness evaluation standards"

If there is no context, please perform the check based solely on the image.
Now please begin evaluating the information completeness of the following context and image:
"""

IMAGE_INFO_COMPLETENESS_CHECK_PROMPT1 = """
Evaluation Objective
    Integrate the provided contextual information to evaluate the completeness of the image, determining whether key information is missing from the image itself, without generating an image description.

Applicable Image Types

    1.Statistical/Data Chart Types

        -Any form of statistical chart (bar chart, line chart, pie chart, scatter plot, etc.)

        -Data visualization charts, infographics

        -Charts with numerical labels

    2.Text-Dense Types

        -Contains a large amount of text (e.g., documents, articles, report pages)

        -Contains a moderate amount of text but with high information density (e.g., infographics, explanatory diagrams, flowcharts)

        -Text serves as the main content carrier, occupying a significant portion of the image area

    3.Informative Non-Artistic Types

        -Technical drawings, design sketches, architectural diagrams

        -Educational materials, knowledge graphs

        -Interface screenshots, webpage screenshots (with readable text content)

        -Images with explanatory text

Evaluation Methodology

    -Dual Evaluation Mode: First, evaluate the completeness of the image itself, then assess whether missing information can be supplemented by the context.

    -Context Role: Context is used only to determine whether missing information can be filled by external information, not to replace the evaluation of the image's inherent completeness.

    -Final Judgment: Even if the context can supplement information, if the image itself has missing information, it is still judged as incomplete.

Information Completeness Judgment Criteria
    Based on the image type, check whether the image itself has the following deficiencies:

Common Criteria for All Image Types:

    -Key text content is blurry, unclear, or unreadable

    -Image resolution is too low, resulting in information loss

    -Important information is obscured or cropped

    -Essential basic elements are missing (e.g., chart title, axis labels, etc.)

Specific Criteria for Statistical/Data Chart Types:

    -Missing horizontal axis title or description

    -Missing vertical axis title or unit

    -Missing necessary legend explanation

    -Data labels missing or incomplete

    -Missing timeline or time annotations

    -Key numerical values cannot be identified

    -Chart title missing

    -Data source annotation missing

Context Supplement Evaluation Criteria:
    If the image itself has deficiencies, check whether the context provides the following supplementary information:

    1.Missing chart title or topic explanation

    2.Missing axis labels or units

    3.Explanation or background of key data

    4.Data source or research methodology explanation

    5.Text content in the chart that cannot be identified

Evaluation Process

    1.Identify Image Type: Determine which of the above types the image belongs to.

    2.Image Completeness Check: Based on the visible content of the image, evaluate item by item according to the corresponding type criteria.

    3.Context Comparison Analysis: If the image has deficiencies, check whether the context can provide corresponding supplementary information.

    4.Comprehensive Judgment: Determine whether there are deficiencies in the image that cannot be compensated by the context.

Output Format
    Please strictly follow the format below to output the evaluation results:

    Information Missing Judgment: [yes / no]

    Missing Information Details:

        1.[If judged as yes, list the missing information items in detail, each explained separately]

        2.[Sort by importance, with the most critical missing items first]

        3.[If judged as no, write "No information missing"]

    Judgment Reasoning:
    [Provide detailed reasoning, including:

        -Based on what criteria the information missing judgment is made

        -The impact level of missing information on understanding the image

        -If missing, whether this information can be supplemented through context]

Evaluation Principles

    1.Clear Prioritization: Use the completeness of the image itself as the primary evaluation benchmark, with context as a supplement.

    2.Slightly Lenient: If the image itself has deficiencies but the context can fully supplement the information, it may be judged as "no."

    3.Categorized Processing: Apply corresponding criteria based on the image type.

    4.Clear Comparison: Clearly distinguish between the deficiencies in the image and the supplementary information in the context.

Special Case Handling

    1.If the image is completely unidentifiable or severely damaged: Directly judge as "yes," with severity rated as "severe deficiency."

    2.If the image is of a non-informative type: Judge as "no," with the remark "not within the scope of evaluation."

    3.If no context is provided: Evaluate only the completeness of the image itself.

    4.If the context is unrelated to the image: Ignore unrelated context and evaluate only the image.

Execution Instructions
    Please evaluate the information completeness of the following image by integrating the provided contextual information. First, analyze the content of the image itself, then compare it with the context to check for supplementary information, and finally provide a comprehensive evaluation result.
"""





