from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ai_agents.prompts import reviewer_prompt

def run_reviewer_agent():
    input_file="output/rewritten_by_writer.txt"
    output_file="output/reviewed_output.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        rewritten_text = f.read()

    prompt = PromptTemplate.from_template(reviewer_prompt)
    llm = Ollama(model="llama3.2")
    chain = LLMChain(llm=llm, prompt=prompt)

    reviewed = chain.run({"text": rewritten_text})

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(reviewed)

    print("✅ Reviewer output saved to", output_file)

if __name__ == "__main__":
    run_reviewer_agent()
