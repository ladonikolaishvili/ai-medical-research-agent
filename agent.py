import os
from typing import Dict, List
from dotenv import load_dotenv
import fitz
import chromadb
import hashlib
import uuid

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up LangSmith observability
from langsmith_config import setup_langsmith
setup_langsmith()

if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langgraph.graph import StateGraph, END
    from langchain_core.tools import tool
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from typing_extensions import TypedDict
    from langsmith import traceable
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1, api_key=OPENAI_API_KEY)
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection_name = "medical_documents"
    
    class AgentState(TypedDict):
        question: str
        pdf_content: str
        analysis: str
        tools_used: List[str]
        pdf_chunks: List[str]
        pdf_metadata: Dict
        document_id: str
        relevant_chunks: List[str]
        session_id: str
        query_id: str

    @tool
    def analyze_medical_text(text: str) -> str:
        """Analyze medical text and provide insights"""
        prompt = ChatPromptTemplate.from_template(
            "Analyze this medical text for key findings, diagnoses, and significant terms: {text}"
        )
        result = (prompt | llm).invoke({"text": text})
        return str(result.content)

    def apply_default_prompt_template(question: str, chunks: str, research: str) -> str:
        """Apply default prompt template from external file for medical analysis"""
        try:
            # Read the prompt template from external file
            with open("default_medical_prompt.txt", "r", encoding="utf-8") as f:
                default_template = f.read()
        except FileNotFoundError:
            # Fallback template if file doesn't exist
            default_template = """You are an expert medical AI assistant with access to relevant document chunks and research data.

INSTRUCTIONS:
1. Analyze the provided medical question and document chunks carefully
2. Provide evidence-based medical information
3. Be precise and professional in your language
4. If uncertain, clearly state limitations
5. Always recommend consulting healthcare professionals for medical decisions

RESPONSE FORMAT:
- Start with a clear, direct answer to the question
- Support your answer with evidence from the provided chunks
- Include relevant medical context and considerations
- End with appropriate disclaimers and recommendations

MEDICAL QUESTION: {question}

RELEVANT DOCUMENT CHUNKS:
{chunks}

RESEARCH CONTEXT:
{research}

Please provide a comprehensive medical analysis following the above instructions."""
        
        return default_template.format(
            question=question,
            chunks=chunks,
            research=research
        )

    def extract_pdf_text(pdf_file) -> str:
        """Extract text from PDF file - direct function for app.py"""
        try:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in pdf_document)
            pdf_document.close()
            return text.strip() or "No text found in PDF"
        except Exception as e:
            return f"PDF extraction failed: {str(e)}"

    @tool
    def semantic_chunk_text(text: str, filename: str = "document") -> Dict:
        """Perform semantic chunking of text using LangChain's RecursiveCharacterTextSplitter"""
        try:
            # Initialize optimized text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100,
                separators=["\n\n", "\n", ". ", " "]
            )
            
            # Split the text into chunks
            chunks = text_splitter.split_text(text)
            
            # Create enhanced metadata for each chunk
            chunk_metadata = []
            for i, chunk in enumerate(chunks):
                # Get first few words for preview
                words = chunk.split()
                preview = " ".join(words[:8]) + ("..." if len(words) > 8 else "")
                
                # Estimate page number (rough calculation)
                char_position = sum(len(chunks[j]) for j in range(i))
                estimated_page = (char_position // 2000) + 1
                
                metadata = {
                    "chunk_index": i,
                    "filename": filename,
                    "chunk_size": len(chunk),
                    "preview": preview,
                    "estimated_page": estimated_page,
                    "reference_id": f"Section-{i+1}",
                    "document_hash": hashlib.md5(text.encode()).hexdigest()[:8]
                }
                chunk_metadata.append(metadata)
            
            return {
                "chunks": chunks,
                "metadata": chunk_metadata,
                "total_chunks": len(chunks)
            }
        except Exception as e:
            return {"error": f"Chunking failed: {str(e)}"}

    @tool
    def store_in_chromadb(chunks: List[str], metadata: List[Dict], document_id: str) -> str:
        """Store semantic chunks and their embeddings in ChromaDB"""
        try:
            # Get or create collection
            try:
                collection = chroma_client.get_collection(name=collection_name)
            except:
                collection = chroma_client.create_collection(name=collection_name)
            
            # Generate embeddings for all chunks
            chunk_embeddings = embeddings.embed_documents(chunks)
            
            # Prepare data for ChromaDB
            ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = []
            for i, meta in enumerate(metadata):
                enhanced_meta = {
                    **meta,
                    "document_id": document_id,
                    "chunk_id": ids[i]
                }
                metadatas.append(enhanced_meta)
            
            # Store in ChromaDB
            collection.add(
                embeddings=chunk_embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            return f"Successfully stored {len(chunks)} chunks in ChromaDB for document {document_id}"
            
        except Exception as e:
            return f"ChromaDB storage failed: {str(e)}"

    @tool
    def query_chromadb(query: str, n_results: int = 5) -> Dict:
        """Query ChromaDB for relevant chunks based on semantic similarity"""
        try:
            # Get collection
            collection = chroma_client.get_collection(name=collection_name)
            
            # Generate embedding for query
            query_embedding = embeddings.embed_query(query)
            
            # Query ChromaDB
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results with similarity scores
            formatted_chunks = []
            if results.get("documents") and len(results["documents"]) > 0:
                documents = results["documents"][0]  # First result set
                metadatas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]
                
                for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
                    similarity_score = 1 - distance  # Convert distance to similarity
                    # Create human-readable reference
                    page_ref = f"Page ~{metadata.get('estimated_page', '?')}" if metadata.get('estimated_page') else ""
                    preview = metadata.get('preview', 'Content preview not available')
                    reference_id = metadata.get('reference_id', f"Section-{metadata.get('chunk_index', 0) + 1}")
                    
                    chunk_info = f"{reference_id} ({page_ref}): '{preview}'"
                    
                    formatted_chunks.append({
                        "rank": i + 1,
                        "content": doc,
                        "similarity_score": round(similarity_score, 3),
                        "metadata": metadata,
                        "chunk_info": chunk_info,
                        "reference_id": reference_id,
                        "page_ref": page_ref,
                        "preview": preview
                    })
            
            return {
                "documents": results.get("documents", []),
                "metadatas": results.get("metadatas", []),
                "distances": results.get("distances", []),
                "formatted_chunks": formatted_chunks,
                "count": len(results.get("documents", []))
            }
            
        except Exception as e:
            return {"error": f"ChromaDB query failed: {str(e)}"}

    @tool
    @traceable(name="research_medical_question")
    def research_medical_question(question: str, session_id: str = "unknown") -> str:
        """Research and answer medical questions"""
        prompt = ChatPromptTemplate.from_template(
            "Provide evidence-based medical information for: {question}"
        )
        result = (prompt | llm).invoke({"question": question})
        return str(result.content)

    @traceable(name="pdf_processor")
    def pdf_processor(state: AgentState) -> AgentState:
        """Process PDF with semantic chunking and ChromaDB storage"""
        if state["pdf_content"] and state["pdf_metadata"]:
            # Generate document ID
            document_id = str(uuid.uuid4())[:8]
            state["document_id"] = document_id
            
            # Perform semantic chunking
            chunking_result = semantic_chunk_text.invoke({
                "text": state["pdf_content"], 
                "filename": state["pdf_metadata"].get("filename", "document.pdf")
            })
            
            if "error" not in chunking_result:
                state["pdf_chunks"] = chunking_result["chunks"]
                
                # Store in ChromaDB
                storage_result = store_in_chromadb.invoke({
                    "chunks": chunking_result["chunks"],
                    "metadata": chunking_result["metadata"],
                    "document_id": document_id
                })
                
                state["tools_used"].extend(["semantic_chunk_text", "store_in_chromadb"])
                state["analysis"] = f"📄 **PDF Processed Successfully**\n\n{storage_result}\n\nTotal chunks: {chunking_result['total_chunks']}"
            else:
                state["analysis"] = f"❌ **PDF Processing Failed**: {chunking_result['error']}"
        
        return state

    @traceable(name="combined_analyzer")
    def combined_analyzer(state: AgentState) -> AgentState:
        """Analyze both question and PDF content together"""
        # Research the question
        research_result = str(research_medical_question.invoke({"question": state["question"], "session_id": state.get("session_id", "unknown")}))
        
        # Query ChromaDB for relevant chunks
        relevant_chunks_section = ""
        if state["document_id"]:
            query_result = query_chromadb.invoke({"query": state["question"], "n_results": 5})
            if "error" not in query_result and query_result.get("formatted_chunks"):
                formatted_chunks = query_result["formatted_chunks"]
                
                # Create human-readable chunks section
                chunks_text = [
                    f"**Rank {chunk['rank']} (Similarity: {chunk['similarity_score']}) - {chunk['chunk_info']}:**\n{chunk['content']}"
                    for chunk in formatted_chunks
                ]
                
                newline = '\n'
                relevant_chunks_section = f"""
**📄 Top 5 Most Relevant PDF Chunks:**

{newline.join(chunks_text)}

---
"""
                
                # Use top 3 chunks for analysis
                analysis_content = "\n\n".join([chunk['content'] for chunk in formatted_chunks[:3]])
                # Store relevant chunks with metadata for prompt engineering
                state["relevant_chunks"] = [{
                    'content': chunk['content'],
                    'reference_id': chunk.get('reference_id', f"Section-{i+1}"),
                    'page_ref': chunk.get('page_ref', ''),
                    'preview': chunk.get('preview', '')
                } for i, chunk in enumerate(formatted_chunks[:5])]
                state["tools_used"].append("query_chromadb")
            else:
                analysis_content = state["pdf_content"][:2000]
        else:
            analysis_content = state["pdf_content"][:2000]
        
        # Analyze PDF content
        pdf_analysis = str(analyze_medical_text.invoke({"text": analysis_content}))
        
        # Combine all analyses
        state["analysis"] = f"""**🔍 Medical Question Analysis:**
{research_result}

**📋 PDF Content Analysis:**
{pdf_analysis}

{relevant_chunks_section}

**💡 Combined Medical Insights:**
Based on the medical question and the provided PDF document analysis, here are the key findings and recommendations combining both the research knowledge and document-specific information."""
        
        state["tools_used"].extend(["research_medical_question", "analyze_medical_text"])
        return state

    @traceable(name="prompt_engineer")
    def prompt_engineer(state: AgentState) -> AgentState:
        """Apply hidden default prompt template after vector similarity search"""
        # Extract relevant chunks text for the prompt with proper references
        relevant_chunks_text = ""
        if state.get("relevant_chunks"):
            chunk_texts = []
            for chunk_data in state["relevant_chunks"][:5]:
                if isinstance(chunk_data, dict):
                    ref_id = chunk_data.get('reference_id', 'Section-?')
                    page_ref = chunk_data.get('page_ref', '')
                    content = chunk_data.get('content', '')
                    chunk_texts.append(f"{ref_id} {page_ref}:\n{content}")
                else:
                    # Fallback for string chunks
                    chunk_texts.append(f"Section-{len(chunk_texts)+1}:\n{chunk_data}")
            relevant_chunks_text = "\n\n".join(chunk_texts)
        
        # Get the research context from the previous analysis
        research_context = state.get("analysis", "").split("**📋 PDF Content Analysis:**")[0]
        research_context = research_context.replace("**🔍 Medical Question Analysis:**", "").strip()
        
        # Apply the hidden default prompt template
        engineered_prompt = apply_default_prompt_template(
            question=state["question"],
            chunks=relevant_chunks_text,
            research=research_context
        )
        
        # Generate response using the hidden prompt template
        prompt_template = ChatPromptTemplate.from_template("{prompt}")
        chain = prompt_template | llm
        result = chain.invoke({"prompt": engineered_prompt})
        
        # Update analysis with prompt-engineered response
        state["analysis"] = str(result.content)
        state["tools_used"].append("prompt_engineer")
        
        return state

    @traceable(name="response_generator")
    def response_generator(state: AgentState) -> AgentState:
        # Ensure clean text output
        analysis_text = str(state["analysis"]).strip()
        
        # Count chunks if available
        chunk_info = ""
        if "query_chromadb" in state["tools_used"]:
            chunk_info = " | Vector similarity search performed on document chunks"
        
        response = f"""🤖 **AI Medical Research Analysis**

{analysis_text}

---
*🔧 Analysis completed using: {', '.join(state["tools_used"])}{chunk_info}*"""
        
        # Store the final response directly in analysis (not in messages)
        state["analysis"] = response
        return state

    def create_medical_agent():
        workflow = StateGraph(AgentState)
        
        workflow.add_node("pdf_processor", pdf_processor)
        workflow.add_node("combined_analyzer", combined_analyzer)
        workflow.add_node("prompt_engineer", prompt_engineer)
        workflow.add_node("response_generator", response_generator)
        
        # Enhanced workflow path with hidden prompt engineering
        workflow.set_entry_point("pdf_processor")
        workflow.add_edge("pdf_processor", "combined_analyzer")
        workflow.add_edge("combined_analyzer", "prompt_engineer")
        workflow.add_edge("prompt_engineer", "response_generator")
        workflow.add_edge("response_generator", END)
        
        return workflow.compile()

    @traceable(name="process_medical_query")
    def process_medical_query(question: str = "", pdf_content: str = "", filename: str = "document.pdf", session_id: str = None) -> str:
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        try:
            if not (question and pdf_content):
                error_msg = "Please provide both a question and PDF content for analysis."
                return error_msg
            
            # Create initial state
            initial_state = {
                "question": question,
                "pdf_content": pdf_content,
                "analysis": "",
                "tools_used": [],
                "pdf_chunks": [],
                "pdf_metadata": {"filename": filename},
                "document_id": None,
                "relevant_chunks": [],
                "session_id": session_id,
                "query_id": str(uuid.uuid4())
            }
            
            # Run the workflow
            agent = create_medical_agent()
            final_state = agent.invoke(initial_state)
            
            analysis = final_state.get('analysis', 'No analysis generated')
            
            return analysis
                
        except Exception as e:
            import traceback
            error_msg = f"Error processing request: {str(e)}"
            return f"{error_msg}\n\nTraceback: {traceback.format_exc()}"

else:
    def process_medical_query(question: str = "", pdf_content: str = "", filename: str = "document.pdf") -> str:
        return "🤖 **AI Agent Setup Required**\n\nPlease configure your OpenAI API key to use the AI Medical Research Agent."
    
    def extract_pdf_text(pdf_file) -> str:
        return "PDF text extraction requires OpenAI API key configuration." 