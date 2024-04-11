"use client";

import React, { useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { RemoteRunnable } from "langchain/runnables/remote";
import { applyPatch } from "@langchain/core/utils/json_patch";

import { EmptyState } from "../components/EmptyState";
import { ChatMessageBubble, Message } from "../components/ChatMessageBubble";
import { AutoResizeTextarea } from "./AutoResizeTextarea";
import { marked } from "marked";
import { Renderer } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/gradient-dark.css";

import "react-toastify/dist/ReactToastify.css";
import {
	Heading,
	Flex,
	IconButton,
	InputGroup,
	InputRightElement,
	Spinner,
	Box,
} from "@chakra-ui/react";
import { ArrowUpIcon } from "@chakra-ui/icons";
import { Select, Link } from "@chakra-ui/react";
import { Source } from "./SourceBubble";
import { apiBaseUrl } from "../utils/constants";
import { ChatPromptValue } from "@langchain/core/prompt_values"
import { AIMessage, FunctionMessage, AIMessageChunk, FunctionMessageChunk } from "@langchain/core/messages"
import { forEach } from "lodash";

const init_msg = "Please input your question."
const typing_msg="Typing answer...."
const processing_msg="Processing..."
const processing_end_msg="Processing end."
const synthesizing_question_msg="Synthesizing question..."
const invoking_tool_msg="Invoking tool..."
function showProcessingTip(processingTip: string) {
	if (processingTip != "" && processingTip != init_msg) {
		return <Box className="whitespace-pre-wrap" color="green" padding={".2em"}>
			{processingTip}
		</Box>
	} else {
		return <Box className="whitespace-pre-wrap" color="red">
			{processingTip}
		</Box>
	}
}
export function ChatWindow(props: { conversationId: string }) {
	const conversationId = props.conversationId;

	const searchParams = useSearchParams();

	const messageContainerRef = useRef<HTMLDivElement | null>(null);
	const [messages, setMessages] = useState<Array<Message>>([]);
	const [input, setInput] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [llm, setLlm] = useState(
		searchParams.get("llm") ?? "anthropic_claude_3_opus",
	);
	const [processingTip, setProcessingTip] = useState("Please input your question.")

	const [chatHistory, setChatHistory] = useState<
		{ role: string; content: string }[]
	>([]);

	const sendMessage = async (message?: string) => {
		if (messageContainerRef.current) {
			messageContainerRef.current.classList.add("grow");
		}
		if (isLoading) {
			return;
		}
		const messageValue = message ?? input;
		if (messageValue === "") return;
		setInput("");
		setMessages((prevMessages) => [
			...prevMessages,
			{ id: Math.random().toString(), content: messageValue, role: "user" },
		]);
		setIsLoading(true);

		let accumulatedMessage = "";
		let runId: string | undefined = undefined;
		let sources: Source[] | undefined = undefined;
		let messageIndex: number | null = null;

		let renderer = new Renderer();
		renderer.paragraph = (text) => {
			return text + "\n";
		};
		renderer.list = (text) => {
			return `${text}\n\n`;
		};
		renderer.listitem = (text) => {
			return `\n• ${text}`;
		};
		renderer.code = (code, language) => {
			const validLanguage = hljs.getLanguage(language || "")
				? language
				: "plaintext";
			const highlightedCode = hljs.highlight(
				validLanguage || "plaintext",
				code,
			).value;
			return `<pre class="highlight bg-gray-700" style="padding: 5px; border-radius: 5px; overflow: auto; overflow-wrap: anywhere; white-space: pre-wrap; max-width: 100%; display: block; line-height: 1.2"><code class="${language}" style="color: #d6e2ef; font-size: 12px; ">${highlightedCode}</code></pre>`;
		};
		marked.setOptions({ renderer });
		try {
			const sourceStepName = "FindDocs";
			let streamedResponse: Record<string, any> = {};
			const remoteChain = new RemoteRunnable({
				url: "http://192.168.3.6:8080/chat",
				options: {
					timeout: 3000000,
				},
			});
			const llmDisplayName = llm ?? "openai_gpt_3_5_turbo";
			const streams = await remoteChain.stream(
				{
					input: messageValue,
					chat_history: chatHistory,
				},
				{
					configurable: {
						llm: llmDisplayName,
					},
					tags: ["model:" + llmDisplayName],
					metadata: {
						conversation_id: conversationId,
						llm: llmDisplayName,
					},
				},
				// {
				//   includeNames: [sourceStepName],
				// },
			);
			for await (const chunk of streams) {
				var _chunk: object
				if (typeof chunk === "object") {
					_chunk = chunk as object;
					console.log(_chunk);
					if ("run_id" in _chunk) {
						runId = _chunk.run_id as string;
					}
					var kind = "event" in _chunk ? _chunk.event : "";
					switch (kind) {
						case "on_chain_start":
							setProcessingTip(prevVal => {
								return synthesizing_question_msg
							})
							break
						case "on_chain_end":
							setProcessingTip(prevVal => {
								if (prevVal == processing_end_msg) {
									return init_msg
								} else if (prevVal != init_msg) {
									console.log(prevVal)
									return processing_msg
								} else {
									return prevVal
								}
							})
							break
						case "on_chain_stream":
							break
						case "on_chat_model_start":
							setProcessingTip(prevVal => {
								return processing_msg
							})
							break
						case "on_chat_model_end":
							setProcessingTip(prevVal => {
								return processing_end_msg
							})
							break
						case "on_chat_model_stream":
							setProcessingTip(prevVal => {
								return typing_msg
							})
							if ("data" in _chunk) {
								var data = _chunk.data as object
								if ("chunk" in data && data.chunk instanceof AIMessageChunk) {
									var aichunk = data.chunk as AIMessageChunk;
									accumulatedMessage += aichunk.content.toString();
								}
							}
							var parsedResult = marked.parse(accumulatedMessage);
							setMessages((prevMessages) => {
								let newMessages = [...prevMessages];
								if (
									messageIndex === null ||
									newMessages[messageIndex] === undefined
								) {
									messageIndex = newMessages.length;
									newMessages.push({
										id: Math.random().toString(),
										content: parsedResult.trim(),
										runId: runId,
										sources: sources,
										role: "assistant",
									});
								} else if (newMessages[messageIndex] !== undefined) {
									newMessages[messageIndex].content = parsedResult.trim();
									newMessages[messageIndex].runId = runId;
									// newMessages[messageIndex].sources = sources;
								}
								return newMessages;
							});
							break
						case "on_tool_start":
							setProcessingTip(prevVal => {
								return invoking_tool_msg 
							})
							break
						case "on_tool_end":
							if ("name" in _chunk && _chunk.name == "search") {
								if ("data" in _chunk) {
									var data = _chunk.data as object;
									if ("output" in data) {
										var output = eval('(' + data.output + ')');
										sources = output.map((doc: Record<string, any>) => ({
											url: doc.link,
											title: doc.title,
										}));
									}
								}
							}
							if ("name" in _chunk && _chunk.name == "searchForGoogleNews") {
								if ("data" in _chunk) {
									var data = _chunk.data as object;
									if ("output" in data) {
										var output = eval('(' + data.output + ')');
										sources = output.map((doc: Record<string, any>) => ({
											url: doc.link,
											title: doc.title,
											img_src: doc.imageUrl,
										}));
									}
								}
							}
							setMessages((prevMessages) => {
								let newMessages = [...prevMessages];
								if (
									messageIndex === null ||
									newMessages[messageIndex] === undefined
								) {
									messageIndex = newMessages.length;
									newMessages.push({
										id: Math.random().toString(),
										content: parsedResult.trim(),
										runId: runId,
										sources: sources,
										role: "assistant",
									});
								} else if (newMessages[messageIndex] !== undefined) {
									// newMessages[messageIndex].content = parsedResult.trim();
									newMessages[messageIndex].runId = runId;
									newMessages[messageIndex].sources = sources;
								}
								return newMessages;
							});
							break
						default:
							break
					}

				}
			}
			setChatHistory((prevChatHistory) => [
				...prevChatHistory,
				{ role: "user", content: messageValue },
				{ role: "assistant", content: accumulatedMessage },
			]);
			setIsLoading(false);
		} catch (e) {
			setMessages((prevMessages) => prevMessages.slice(0, -1));
			setIsLoading(false);
			setInput(messageValue);
			throw e;
		}
	};

	const sendInitialQuestion = async (question: string) => {
		await sendMessage(question);
	};

	const insertUrlParam = (key: string, value?: string) => {
		if (window.history.pushState) {
			const searchParams = new URLSearchParams(window.location.search);
			searchParams.set(key, value ?? "");
			const newurl =
				window.location.protocol +
				"//" +
				window.location.host +
				window.location.pathname +
				"?" +
				searchParams.toString();
			window.history.pushState({ path: newurl }, "", newurl);
		}
	};

	return (
		<div className="flex flex-col items-center p-8 rounded grow max-h-full">
			<Flex
				direction={"column"}
				alignItems={"center"}
				marginTop={messages.length > 0 ? "" : "64px"}
			>
				<Heading
					fontSize={messages.length > 0 ? "2xl" : "3xl"}
					fontWeight={"medium"}
					mb={1}
					color={"white"}
				>
					🍺 Eddie's Assistant 🥩
				</Heading>
				<Heading
					fontSize="xl"
					fontWeight={"normal"}
					color={"white"}
					marginTop={"10px"}
					textAlign={"center"}
				>
					Ask me anything!{" "}
				</Heading>

				<div className="text-white flex flex-wrap items-center mt-4">
					<div className="flex items-center mb-2">
						<span className="shrink-0 mr-2">Powered by</span>
						<Select
							value={llm}
							onChange={(e) => {
								insertUrlParam("llm", e.target.value);
								setLlm(e.target.value);
							}}
							width={"240px"}
						>
							<option value="anthropic_claude_3_opus">Anthropic-Claude-3-Opus</option>
							<option value="openai_gpt_4_turbo_preview">GPT-4-Turbo</option>
							<option value="openai_gpt_3_5_turbo_1106">GPT-3.5-Turbo</option>
							<option value="pplx_sonar_medium_chat">PPLX_sonar_medium_chat</option>
							<option value="mistral_large">Mistral-Large</option>
							<option value="command_r_plus">Command R+</option>
						</Select>
					</div>
				</div>
				<div className="flex flex-wrap items-center mt-4">
					{showProcessingTip(processingTip)}
				</div>
			</Flex>
			<div
				className="flex flex-col-reverse w-full mb-2 overflow-auto"
				ref={messageContainerRef}
			>
				{
					[...messages]
						.reverse()
						.map((m, index) => (
							<ChatMessageBubble
								key={m.id}
								message={{ ...m }}
								aiEmoji="🦜"
								isMostRecent={index === 0}
								messageCompleted={!isLoading}
							></ChatMessageBubble>
						))
				}
			</div>
			<InputGroup size="md" alignItems={"center"}>
				<AutoResizeTextarea
					value={input}
					maxRows={5}
					marginRight={"56px"}
					placeholder="Hello, World!"
					textColor={"white"}
					borderColor={"rgb(58, 58, 61)"}
					onChange={(e) => setInput(e.target.value)}
					onKeyDown={(e) => {
						if (e.key === "Enter" && !e.shiftKey) {
							e.preventDefault();
							sendMessage();
						} else if (e.key === "Enter" && e.shiftKey) {
							e.preventDefault();
							setInput(input + "\n");
						}
					}}
				/>
				<InputRightElement h="full">
					<IconButton
						colorScheme="blue"
						rounded={"full"}
						aria-label="Send"
						icon={isLoading ? <Spinner /> : <ArrowUpIcon />}
						type="submit"
						onClick={(e) => {
							e.preventDefault();
							sendMessage();
						}}
					/>
				</InputRightElement>
			</InputGroup>
		</div>
	);
}
