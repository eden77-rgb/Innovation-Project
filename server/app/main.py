from domain import PromptBuilder, PromptType

prompt = PromptBuilder.build(PromptType.SUMMARY, "aaaaaaaaaaaaaaa")
print(prompt)