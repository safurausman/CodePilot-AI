import json, os
from google import genai
from google.genai import types
from modules.tools.safe_python import execute_safe_python
from modules.tools.file_tools import list_output_files, read_output_file, write_output_file
from modules.tools.test_runner import run_unittest

TOOLS = {
 "safe_python": lambda args: {"result": execute_safe_python(args.get("expression",""))},
 "list_files": lambda args: {"files": list_output_files()},
 "read_file": lambda args: {"content": read_output_file(args.get("filename",""))},
 "write_file": lambda args: {"saved_path": write_output_file(args.get("filename",""),args.get("content",""))},
 "run_tests": lambda args: _run_tests(args),
}
def _run_tests(args):
    output, code=run_unittest(args.get("filename",""))
    return {"exit_code":code,"output":output}

def run_agent(goal, max_steps=5):
    key=os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("Set GEMINI_API_KEY before using the agent.")
    client=genai.Client(api_key=key)
    model=os.getenv("GEMINI_MODEL","gemini-3.5-flash-lite")
    catalog={
      "safe_python":{"description":"Evaluate a restricted mathematical/Python expression, no imports or arbitrary code.","args":{"expression":"string"}},
      "list_files":{"description":"List generated files in codepilot_outputs.","args":{}},
      "read_file":{"description":"Read a generated file by filename from codepilot_outputs.","args":{"filename":"string"}},
      "write_file":{"description":"Create a new file in codepilot_outputs. Never overwrite existing files.","args":{"filename":"string","content":"string"}},
      "run_tests":{"description":"Run unittest against an existing .py test module in codepilot_outputs; timeout 20 seconds.","args":{"filename":"string"}}
    }
    planning_prompt=f"""You are CodePilot's task-planning agent. Return ONLY valid JSON object with keys plan (array of short steps), actions (array), final_if_no_tools (string).
Each action has tool (one of {list(TOOLS)}) and args (object). Use at most {max_steps} actions. Do not write files or run tests unless the user explicitly requests it. For a request requiring user approval for file writing, do not invoke write_file; explain it needs approval. Do not invent tool results.
Available tools: {json.dumps(catalog)}
User goal: {goal}"""
    response=client.models.generate_content(model=model,contents=planning_prompt,
        config=types.GenerateContentConfig(temperature=0.1,response_mime_type="application/json"))
    plan_data=json.loads(response.text)
    steps=[]
    for i,action in enumerate(plan_data.get("actions",[])[:max_steps],1):
        tool=action.get("tool")
        if tool not in TOOLS:
            steps.append({"step":i,"tool":str(tool),"status":"blocked","result":"Unknown tool."})
            continue
        if tool=="write_file":
            steps.append({"step":i,"tool":tool,"status":"approval_required","result":"File creation requires explicit user approval."})
            continue
        try:
            result=TOOLS[tool](action.get("args") or {})
            steps.append({"step":i,"tool":tool,"status":"success","result":result})
        except Exception as exc:
            steps.append({"step":i,"tool":tool,"status":"error","result":str(exc)})
    summary_prompt=f"""User goal: {goal}
Plan: {json.dumps(plan_data.get('plan',[]))}
Actual tool execution results: {json.dumps(steps,default=str)}
Write a concise final response. Distinguish successful actions from errors. Never claim unexecuted work."""
    final=client.models.generate_content(model=model,contents=summary_prompt,
        config=types.GenerateContentConfig(temperature=0.2))
    return plan_data.get("plan",[]), steps, final.text or "Agent completed."
