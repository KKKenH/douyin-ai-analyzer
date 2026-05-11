import os
import glob
import requests

API_KEY = os.getenv("DOUBAO_API_KEY")
MODEL = "doubao-lite-4k"
URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

def analyze(script):
    prompt = f"""
你是抖音爆款分析师，严格按下面格式输出：
【爆款评分】1-10分
【优点】3条
【缺点】3条
【优化建议】3条
【推荐标签】5个

脚本：
{script}
"""
    res = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    })
    return res.json()["choices"][0]["message"]["content"]

def main():
    out = "# 抖音内容分析报告\n\n"
    for f in glob.glob("scripts/*.txt"):
        with open(f, "r", encoding="utf-8") as f2:
            txt = f2.read()
        out += f"## {os.path.basename(f)}\n{analyze(txt)}\n\n---\n\n"
    with open("analysis-report.md", "w", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    main()
