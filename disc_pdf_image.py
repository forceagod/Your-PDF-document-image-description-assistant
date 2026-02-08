from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    filter_messages,
    get_buffer_string,
)
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
import base64
import re
from prompt import (
    IMAGE_DISC_PROMPT,
    IMAGE_INFO_EXTRACT_PROMPT,
    IMAGE_JUDGE_PROMPT,
    IMAGE_INFO_COMPLETENESS_CHECK_PROMPT,
    IMAGE_INFO_COMPLETENESS_CHECK_PROMPT1
)
from state import (
    judge_out,
    disc_image_out,
    summmary_image_info_from_context_out,
    AgentInputState,
    AgentState
)
from context_tool import get_image_context
from config import chat_model_api_key,v_model_api_key
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage
import time
import os

chat_model = ChatOpenAI(
    model = "deepseek-chat",
    temperature = 0.3,
    api_key = chat_model_api_key,
    base_url = "https://api.deepseek.com"
)

v_model = ChatZhipuAI(
    model="glm-4.6v",
    temperature=0.3,
    api_key="8f7affaca409488c918b013459f7952c.8AjXQWudy32y6VK6",
    thinking={
            "type":"enabled"
        }
)


def judge_image(state: AgentState) -> Command[Literal["image_info_completeness_check", "__end__"]]:

    # Step 2: Prepare the model for structured clarification analysis
    image_path = state["image_path"]
    with open(image_path, "rb") as image_file:
        # 编码为base64
        target_image = base64.b64encode(image_file.read()).decode('utf-8')


    judge_message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_JUDGE_PROMPT},
            {
                "type": "image_url",
                "image_url": {"url": target_image},
            },
        ],
    )
    time.sleep(3) 
    response = v_model.invoke([judge_message])

    pattern = r"Judgment Result:\s*([^\n]+)"
    match = re.search(pattern, response.content)
    result = match.group(1).strip()
    # Step 4: Route based on clarification analysis
    if result == 'Not Meaningful':
        print("图像无意义")
        # End with clarifying question for user
        return Command(
            goto=END, 
            #update={"messages": [AIMessage(content=response.content)]}
        )
    else:
        # Proceed to research with verification message
        print("图像有意义，准备进行信息完整性检查")
        return Command(
            goto="image_info_completeness_check", 
            #update={"messages": [AIMessage(content=result)]}
        )


def image_info_completeness_check(state: AgentState) -> Command[Literal["disc_image","get_image_context"]]:

    # Step 1: Set up the research model for structured output
    print("正在进行信息完整性检查")
    print("context: "+ state["image_context"])
    image_path = state["image_path"]
    with open(image_path, "rb") as image_file:
        # 编码为base64
        target_image = base64.b64encode(image_file.read()).decode('utf-8')
    check_message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_INFO_COMPLETENESS_CHECK_PROMPT1 + "  " + "context: " + state["image_context"]},
            {
                "type": "image_url",
                "image_url": {"url": target_image},
            },
        ],
    )
    time.sleep(3) 
    response = v_model.invoke([check_message])

    pattern = r"Information Missing Judgment:\s*([^\n]+)"
    match = re.search(pattern, response.content)
    result = match.group(1).strip()
    if result == 'no':
        # End with clarifying question for user
        print("信息完整，准备描述")
        return Command(
            goto="disc_image", 
            #update={"messages": [AIMessage(content=response.content)]}
        )
    else:
        # Proceed to research with verification message
        print("信息不完整，准备收集上下文")
        return Command(
            goto="get_image_context", 
            update={"Number_of_check": state.get("Number_of_check",0) + 1}
        )


def get_image_context(state: AgentState) -> Command[Literal["image_info_completeness_check","__end__"]]:

    def find_image_context_with_range(markdown_content, image_filename, context_range=1):
        lines = [line.strip() for line in markdown_content.split('\n')]
    
        pattern = rf'.*{re.escape(image_filename)}.*'
    
        result = {
            'found': False,
            'image_line': None,
            'up_contexts': [],  # 存储多行上文
            'down_contexts': [],  # 存储多行下文
            'line_number': None
        }
    
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                result['found'] = True
                result['image_line'] = line
                result['line_number'] = i + 1
            
            # 提取多行上文
                start_up = max(0, i - context_range)
                for j in range(start_up, i):
                    if lines[j]:  # 只添加非空行
                        result['up_contexts'].append({
                            'line_num': j + 1,
                            'content': lines[j]
                        })
            
            # 提取多行下文
                end_down = min(len(lines), i + context_range + 1)
                for j in range(i + 1, end_down):
                    if lines[j]:  # 只添加非空行
                        result['down_contexts'].append({
                            'line_num': j + 1,
                            'content': lines[j]
                        })
            
                break
    
        return result
    try:
        print("准备收集上下文...")
        # 读取Markdown文件
        with open(state["mark_down_path"], 'r', encoding='utf-8') as file:
            markdown_content = file.read()
        # 查找图像路径和上下文
        result = find_image_context_with_range(markdown_content, state["image_name"],min(state["Number_of_check"],10))
        up_c = "The above text:" + ",".join(x["content"] for x in result["up_contexts"])
        down_c = "The following text:" + ",".join(x["content"] for x in result["down_contexts"])
        r = up_c + "  " + down_c
        image_path = state["image_path"]
        with open(image_path, "rb") as image_file:
        # 编码为base64
            target_image = base64.b64encode(image_file.read()).decode('utf-8')
        context_summary_message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_INFO_EXTRACT_PROMPT + " " + r},
            {
                "type": "image_url",
                "image_url": {"url": target_image},
            },
        ],
        )
        time.sleep(3) 
        response = v_model.invoke([context_summary_message])
        print("上下文收集完毕，再次进行检查")
        return Command(
            goto="image_info_completeness_check", 
            update={"image_context": response.content}
        )
        
    except FileNotFoundError:
        print("收集失败1")
        Command(
            goto=END, 
            update={"e_error": "nothing"}
        )
    except Exception as e:
        print(e)
        Command(
            goto=END, 
            update={"e_error": "nothing"}
        )

def disc_image(state: AgentState) -> Command[Literal["__end__"]]:

    # Step 1: Set up the research model for structured output
    image_path = state["image_path"]
    with open(image_path, "rb") as image_file:
        # 编码为base64
        target_image = base64.b64encode(image_file.read()).decode('utf-8')
    image_disc_message = HumanMessage(
        content=[
            {"type": "text", "text": IMAGE_DISC_PROMPT + "  " + "Supplementary information: " + state["image_context"]},
            {
                "type": "image_url",
                "image_url": {"url": target_image},
            },
        ],
    )
    time.sleep(3) 
    response = v_model.invoke([image_disc_message])
    print("描述完成")
    return Command(
            goto=END, 
            update={"final_image_disc": response.content}
    )  


deep_image_disc_builder = StateGraph(
    AgentState, 
    input=AgentInputState, 
)

# Add main workflow nodes for the complete research process
deep_image_disc_builder.add_node("judge_image", judge_image)           # User clarification phase
deep_image_disc_builder.add_node("image_info_completeness_check", image_info_completeness_check)     # Research planning phase
deep_image_disc_builder.add_node("get_image_context", get_image_context)       # Research execution phase
deep_image_disc_builder.add_node("disc_image", disc_image)  # Report generation phase

# Define main workflow edges for sequential execution
deep_image_disc_builder.add_edge(START, "judge_image")                       # Entry point# Research to report
deep_image_disc_builder.add_edge("disc_image", END)                   # Final exit point

# Compile the complete deep researcher workflow
deep_image_disc = deep_image_disc_builder.compile()
    
def main():
    with open('demo7\hybrid_auto\demo7.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有图片路径（假设路径以images/开头）
    image_paths = re.findall(r'images/[a-zA-Z0-9_\-\./]+\.(?:jpg|jpeg|png|gif)', content)
    table_pattern = r'<table>.*?</table>'
    tables = re.findall(table_pattern, content, re.DOTALL)
    # 替换每个路径
    for orig_path in image_paths:
        # 将正斜杠转换为反斜杠
        win_path = orig_path.replace('/', '\\')
        # 添加前缀
        new_path = f"demo7\\hybrid_auto\\{win_path}"
        # 替换内容
        ima_name = os.path.basename(new_path)
        input_state = {
            "image_path": new_path, 
            "image_name": ima_name,
            "mark_down_path": 'demo7\hybrid_auto\demo7.md',  # 包含图像上下文的Markdown文件
            "image_context":" ",
            "Number_of_check": 5,
            "final_image_disc":" ",
            "p_error":" "
        }
        max_retries = 5
        retry_count = 0
        while retry_count <= max_retries:
            try:
                r = deep_image_disc.invoke(input_state)
                break
            except Exception as e:
                print("重来一次")
                retry_count += 1
        f_disc = r["final_image_disc"]
        #image_disc = disc_image(image_base64)
        content = content.replace(orig_path, f_disc)
        print(f"已转换: {orig_path} -> {f_disc}")
    #for table in tables:
        #table_disc = disc_table(table)
        #content = content.replace(table, table_disc)
    # 保存结果
    with open('your_file_converted.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n已完成所有转换！")


if __name__ == "__main__":

    main()
