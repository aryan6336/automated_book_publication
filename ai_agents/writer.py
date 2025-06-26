from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from ai_agents.prompts import writer_prompt

def run_writer_agent():
    # Read chapter
    input_file="output/chapter1.txt" 
    output_file="output/rewritten_by_writer.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Create LangChain components
    prompt = PromptTemplate.from_template(writer_prompt)
    llm = Ollama(model="llama3.2")
    chain = LLMChain(llm=llm, prompt=prompt)

    # Generate rewritten chapter
    rewritten = chain.run({"text": raw_text})

    # Save output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rewritten)

    print("✅ Writer output saved to", output_file)

if __name__ == "__main__":
    run_writer_agent()
