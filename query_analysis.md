# 查询分析

“搜索”支持许多用例 - 包括检索增强生成的“检索”部分。最简单的方法涉及直接将用户问题传递给检索器。为了提高性能，您还可以通过某种方式使用**查询分析**来“优化”查询。传统上，这是通过基于规则的技术完成的，但随着LLMs的兴起，使用LLM进行优化变得越来越流行和可行。具体来说，这涉及将原始问题（或消息列表）传入LLM，并返回一个或多个优化查询，这通常包含一个字符串和可选的其他结构化信息。

![查询分析](https://python.langchain.com/assets/images/query_analysis-cf7fe2eec43fce1e2e8feb1a16413fab.png)

## 解决的问题

查询分析有助于优化发送到检索器的搜索查询。当出现以下情况时，就会出现这种情况：

- 检索器支持针对数据的特定字段进行搜索和过滤，用户输入可能涉及这些字段中的任何一个，
- 用户输入中包含多个不同的问题，
- 为检索相关信息需要多个查询，
- 搜索质量对措词敏感，
- 有多个检索器可以搜索，用户输入可能涉及其中任何一个。

注意，不同的问题将需要不同的解决方案。为了确定您应该使用哪种查询分析技术，您将希望准确了解您当前检索系统的问题是什么。最好是通过查看您当前应用的失败数据点并识别常见主题来完成。只有当您知道您的问题是什么时，您才能开始解决它们。

## 快速开始

前往[快速开始](https://python.langchain.com/docs/use_cases/query_analysis/quickstart/)，了解如何在一个基本的端到端示例中使用查询分析。这将涵盖对LangChain YouTube视频内容建立搜索引擎，展示当将原始用户问题传递到该索引时出现的一个失败模式，然后是查询分析如何帮助解决该问题的示例。快速入门侧重于**查询构建**。以下是根据您的数据和用例可能相关的其他查询分析技术

## 技术

我们支持多种技术，用于从原始问题或消息列表转换为更优化的查询。这些包括：

- [查询分解](https://python.langchain.com/docs/use_cases/query_analysis/techniques/decomposition/)：如果用户输入包含多个不同的问题，我们可以将输入分解为将各自独立执行的单独查询。
- [查询扩展](https://python.langchain.com/docs/use_cases/query_analysis/techniques/expansion/)：如果索引对查询措词敏感，我们可以生成用户问题的多个释义版本，以增加检索到相关结果的机会。
- [假设文档嵌入（HyDE）](https://python.langchain.com/docs/use_cases/query_analysis/techniques/hyde/)：如果我们使用基于相似度搜索的索引（如向量存储），那么直接搜索原始问题可能效果不佳，因为它们的嵌入可能与相关文档的嵌入不太相似。相反，让模型生成一个假设的相关文档，然后使用它进行相似度搜索可能会有所帮助。
- [查询路由](https://python.langchain.com/docs/use_cases/query_analysis/techniques/routing/)：如果我们有多个索引，而只有一部分对任何给定的用户输入有用，我们可以仅从相关的索引中检索输入。
- [退后提示](https://python.langchain.com/docs/use_cases/query_analysis/techniques/step_back/)：有时，搜索质量和模型生成可能会被问题的细节所困扰。处理这种情况的一种方法是首先生成一个更抽象的“退后”问题，并基于原始问题和退后问题进行查询。
- [查询构建](https://python.langchain.com/docs/use_cases/query_analysis/techniques/structuring/)：如果我们的文档有多个可搜索/可过滤的属性，我们可以从任何原始用户问题中推断出哪些特定属性应该被搜索/过滤。例如，当用户输入与视频发布日期有关时，该输入应成为每个文档的`publish_date`属性的一个过滤条件。

## 如何

- [向提示中添加示例](https://python.langchain.com/docs/use_cases/query_analysis/how_to/few_shot/)：随着我们的查询分析变得更复杂，向提示中添加示例可以显著提高性能。
- [处理高基数分类](https://python.langchain.com/docs/use_cases/query_analysis/how_to/high_cardinality/)：您将创建的许多结构化查询将涉及分类变量。当存在许多潜在值时，正确执行此操作可能很困难。
- [构建过滤器](https://python.langchain.com/docs/use_cases/query_analysis/how_to/constructing-filters/)：本指南介绍如何从Pydantic模型转换为您正在使用的向量存储的查询语言中的过滤器。
- [处理多个查询](https://python.langchain.com/docs/use_cases/query_analysis/how_to/multiple_queries/)：一些查询分析技术会生成多个查询。本指南处理如何将它们全部传递给检索器。
- [处理无查询](https://python.langchain.com/docs/use_cases/query_analysis/how_to/no_queries/)：一些查询分析技术可能根本不会生成查询。本指南处理如何优雅地处理这些情况。
- [处理多个检索器](https://python.langchain.com/docs/use_cases/query_analysis/how_to/multiple_retrievers/)：一些查询分析技术涉及在多个检索器之间路由。本指南涵盖如何优雅地处理这一点。

---

请注意，原始链接中的文章可能包含一些动态元素或最新信息，这些在翻译中可能未能完全体现。