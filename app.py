from flask import Flask, render_template, request, jsonify, session
import os
import uuid
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

from claims import get_claim_data
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'policies'))
from policies.policy import search_policies

app = Flask(__name__)
app.secret_key = os.urandom(24)

llm = Ollama(model="gemma3:1b")

chat_histories = {}

def get_session_history(session_id: str):
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

POLICY_MAPPING = {
    1: "one",
    2: "two", 
    3: "three",
    4: "four",
    5: "five"
}

def format_claim_context(claim_data):
    claim = claim_data['data']
    
    billed = float(claim['payment']['billed_amount'] or 0)
    approved = float(claim['payment']['approved_amount'] or 0)
    copay = float(claim['payment']['copay_amount'] or 0)
    coinsurance = float(claim['payment']['coinsurance_amount'] or 0)
    deductible = float(claim['payment']['deductible_amount'] or 0)
    net_payment = float(claim['payment']['net_payment'] or 0)
    
    return f"""CLAIM INFORMATION:
Claim ID: {claim['claim_id']} | Status: {claim['status']['claim_status']}
Service Date: {claim['date_of_service']} | Received: {claim['received_date']}

MEMBER: {claim['member']['full_name']} (ID: {claim['member']['member_id']})
DOB: {claim['member']['date_of_birth']} | Gender: {claim['member']['gender']}

COVERAGE: {claim['coverage']['coverage_name']} (ID: {claim['coverage']['coverage_id']})
Effective: {claim['coverage']['effective_date']} to {claim['coverage']['term_date']}

PAYMENT BREAKDOWN:
Billed: ₹{billed:.2f} | Approved: ₹{approved:.2f}
Copay: ₹{copay:.2f} | Coinsurance: ₹{coinsurance:.2f} | Deductible: ₹{deductible:.2f}
Net Payment: ₹{net_payment:.2f}"""

def build_system_prompt(has_claim=False):
    
    base = """You are InsureCheck, a helpful insurance support assistant.

IMPORTANT RULES:
1. Answer questions using ONLY the information provided in the context below
2. If the context has the answer, explain it clearly and naturally in complete sentences
3. If the context does NOT contain the answer, say: "I don't have that information in the current policy documents"
4. NEVER make up or invent information not present in the context
5. Provide helpful, conversational responses - not just copy-paste from the policy
6. When explaining policy terms, be clear and easy to understand

RESPONSE STYLE:
- Write in a friendly, professional tone
- Do NOT use formattings such as bold, italics or bullets
- Use complete sentences and paragraphs
- Break down complex information into simple explanations
- Reference specific policy sections when relevant (mention page numbers)
- If calculation or amounts are involved, show them clearly"""

    if has_claim:
        base += """

YOU HAVE ACCESS TO:
- The member's active claim details
- Relevant sections from their insurance policy document

Use this information to provide specific, accurate answers about their claim and coverage."""
    
    return base

def retrieve_policy_context(question, policy_name, k=5):
    try:
        results = search_policies(
            query=question,
            policy_names=policy_name,
            k=k
        )
        
        if not results or len(results) == 0:
            return None
        
        sections = []
        for i, doc in enumerate(results, 1):
            summary_type = doc.metadata.get('summary_type', 'unknown')
            page_range = doc.metadata.get('page_range', 'unknown')
            
            sections.append(
                f"[Policy Section {i} - {summary_type.upper()} level - Pages {page_range}]\n{doc.page_content}"
            )
        
        return "\n\n".join(sections)
        
    except Exception as e:
        print(f"Error retrieving policy: {e}")
        return None

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/set_claim', methods=['POST'])
def set_claim():
    try:
        data = request.json
        claim_id = data.get('claim_id')
        
        if not claim_id:
            return jsonify({'success': False, 'error': 'Please provide a claim ID'})
        
        try:
            claim_id_int = int(claim_id)
        except ValueError:
            return jsonify({'success': False, 'error': 'Claim ID must be a number'})
        
        result = get_claim_data(claim_id_int)
        if not result['success']:
            return jsonify(result)
        
        policy_id = result['data']['member']['policy_id']
        policy_name = POLICY_MAPPING.get(policy_id)
        
        if not policy_name:
            return jsonify({'success': False, 'error': f'Policy ID {policy_id} not recognized'})
        
        session['claim_id'] = claim_id
        session['claim_data'] = result['data']
        session['policy_name'] = policy_name
        session['policy_id'] = policy_id
        
        return jsonify({
            'success': True,
            'policy_name': policy_name,
            'claim_status': result['data']['status']['claim_status'],
            'member_name': result['data']['member']['full_name'],
            'coverage_name': result['data']['coverage']['coverage_name']
        })
        
    except Exception as e:
        print(f"Error in set_claim: {e}")
        return jsonify({'success': False, 'error': f'Error processing claim: {str(e)}'})

@app.route('/api/clear_claim', methods=['POST'])
def clear_claim():
    session.pop('claim_id', None)
    session.pop('claim_data', None)
    session.pop('policy_name', None)
    session.pop('policy_id', None)
    return jsonify({'success': True})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question', '').strip()
        session_id = session.get('session_id')
        
        if not question:
            return jsonify({'success': False, 'error': 'Please provide a question'})
        
        claim_data = session.get('claim_data')
        policy_name = session.get('policy_name')
        has_claim = claim_data is not None
        
        context_parts = []
        
        if has_claim:
            context_parts.append("="*80)
            context_parts.append(format_claim_context({'data': claim_data}))
            context_parts.append("="*80)
            
            policy_context = retrieve_policy_context(question, policy_name, k=5)
            
            if policy_context:
                context_parts.append("\nRELEVANT POLICY SECTIONS:")
                context_parts.append(policy_context)
                context_parts.append("\nUse the above policy information to answer the question clearly and completely.")
            else:
                context_parts.append("\n[No specific policy sections found for this query]")
        
        full_context = "\n\n".join(context_parts) if context_parts else ""
        
        history = get_session_history(session_id)
        
        system_prompt = build_system_prompt(has_claim)
        if full_context:
            system_prompt += f"\n\n{full_context}"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])
        
        chain = prompt | llm
        response = chain.invoke({
            "question": question,
            "history": history.messages
        })
        
        response = response.strip()
        
        history.add_user_message(question)
        history.add_ai_message(response)
        
        return jsonify({
            'success': True,
            'response': response,
            'has_claim': has_claim,
            'policy_name': policy_name if has_claim else None
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'success': False, 'error': f'Error processing chat: {str(e)}'})

@app.route('/api/clear_chat', methods=['POST'])
def clear_chat():
    session_id = session.get('session_id')
    if session_id and session_id in chat_histories:
        chat_histories[session_id].clear()
    return jsonify({'success': True})

@app.route('/api/new_session', methods=['POST'])
def new_session():
    old_session_id = session.get('session_id')
    if old_session_id and old_session_id in chat_histories:
        del chat_histories[old_session_id]
    
    session.clear()
    session['session_id'] = str(uuid.uuid4())
    
    return jsonify({'success': True, 'session_id': session['session_id']})

if __name__ == '__main__':
    app.run(debug=True, port=5000)