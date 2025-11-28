## Korius – AI Control Tower for Pharmacy Procurement


<video src="assets/video_demo.mp4" controls style="max-width: 100%; margin-top: 8px;">
  Your browser does not support the video tag.
</video>

**Korius** is an AI-powered control tower that automates supplier calls, price checks, and market catalog updates for pharmacies.  
It turns raw order and supplier data, plus external market product feeds, into **actionable recommendations** and **ready-to-execute tasks** for the procurement team.

Think of it as a **virtual sourcing analyst** that:
- Monitors supplier performance and margins in real time
- Detects cheaper alternatives across your supplier base
- Parses agent phone conversations to update ETAs and prices
- Surfaces prioritized recommendations in a clean, operator-first UI

---

## Description

Korius is a proactive AI control tower designed to **reduce procurement risk and cost** for pharmacies.  
Instead of manually calling suppliers, checking prices, and updating catalogs, buyers rely on AI agents that monitor the market, talk to suppliers, and surface the next best actions.

The system is built as a **hackathon-ready prototype** to showcase how AI can:
- Continuously compare in-store prices with market offers
- Parse supplier phone calls to keep ETAs and conditions up to date
- Highlight margin opportunities on everyday products
- Free up operators from repetitive, low-value follow-up work

**Target user**: Pharmacy or healthcare procurement manager who owns supplier relationships, margin, and purchasing budget.

---

## Overview

This AI-powered system augments a pharmacy’s purchasing workflow by combining:

- **Supplier and product analytics** over local CSV data
- **Market product and price comparison** to highlight cheaper or faster alternatives
- **AI transcript parsing** to turn unstructured calls into structured delivery and pricing updates
- **A control-center UI** that lets buyers see agent impact and act on recommendations in one place

The result is a **single pane of glass** for monitoring supplier performance, market offers, and open follow-ups.

---

## Features

### Control Center for Procurement Teams

- Dashboard that shows how many:
  - Delivery risks have been de‑risked by agents
  - Supplier follow-ups were sent automatically
  - Price checks were completed against current market conditions
  - New product matches were identified for existing needs
- Daily recap timeline with example transcripts so stakeholders can **see how the AI actually talks and reasons**.

### Supplier and Market Intelligence

- Supplier performance and margin analysis driven by:
  - Delivery performance (on-time vs late)
  - Price competitiveness across suppliers
  - Order volume and product diversity
- Market product listing from `available_product.csv` to:
  - Compare unit prices across suppliers
  - Identify cheaper or more reliable alternatives for in-store products
  - Quantify potential savings and margin uplift.

### AI Call & Transcript Parsing

- Uses Mistral AI to analyze **real call transcripts** between the pharmacy and suppliers.
- Extracts structured fields such as:
  - Updated estimated delivery dates
  - Delay/advance in days vs the original ETA
- Outputs machine-usable updates that can be applied back to `orders.csv`.

### Alerting & Recommendations

- AI Recommendations panel that adapts to the current tab (Control Center, Suppliers, Products).
- Suggestions include:
  - Switching supplier for specific molecules to save cost
  - Re‑contacting suppliers with poor reliability
  - Adjusting product mix based on demand patterns or market availability
- Each suggestion is actionable in the UI and designed to map to future **end‑to‑end workflows** (e.g., auto-adjusting orders, triggering negotiations).

---

## How It Works

![System architecture](assets/architecture.png)

1. **Data ingestion**  
   CSV files in `data/` (`fournisseur.csv`, `in_store_product.csv`, `available_product.csv`, `orders.csv`) are loaded and converted into typed models.

2. **Supplier and product analysis**  
   Backend services compute:
   - Cheaper alternatives for in-store products
   - Supplier performance and margin impact
   - Innovative products available in the market but not yet listed in store.

3. **AI agent conversations**  
   Phone calls with suppliers are transcribed into JSON files.  
   The `OrderDeliveryParser` service uses Mistral AI to:
   - Read the transcript
   - Detect product-by-product delivery changes
   - Produce structured JSON with new dates and delays.

4. **Updates and insights**  
   Parsed outputs are applied back to orders and can update product metadata.  
   Aggregated metrics are exposed by FastAPI endpoints, consumed by the frontend via `src/lib/api.ts`.

5. **Buyer experience**  
   The React frontend renders:
   - A Control Center summarizing AI activity and sample transcripts
   - A Suppliers view showing performance, issues, and contact actions
   - A Products view focused on market listings and margin comparison
   - An AI Recommendations panel that surfaces the most impactful actions first.

---

## Key Benefits

- **Reduced manual follow-up**: AI agents and parsing pipelines handle day-to-day supplier calls and status checks.
- **Better margins with less effort**: Systematically highlights cheaper market alternatives and margin opportunities hidden in CSVs.
- **Fewer unpleasant surprises**: Parsed ETAs and delivery delays make risks visible early, so teams can act before stock‑outs.
- **Judge- and stakeholder-friendly UI**: Clear storytelling in the Control Center and Suppliers views, with realistic transcripts and metrics.

---

## Tech Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn-ui  
  - SPA hosted under `frontend/`  
  - Uses `@tanstack/react-query` for data fetching  
  - Talks to the backend at `http://localhost:8000/api/*`

- **Backend**: FastAPI (Python 3.10+)  
  - Lives under `backend/`  
  - Exposes REST endpoints for suppliers, products, and parsing pipelines  
  - Serves as the orchestration layer between:
    - Local CSV data (`data/` directory)
    - Analysis services (supplier performance and margin analysis, cheaper alternatives, product discovery)
    - Optional AI agents (Mistral AI, ElevenLabs) for call parsing

- **Data layer**: Ingested from CSVs under `data/`  
  - `fournisseur.csv`: suppliers  
  - `in_store_product.csv`: current catalog and prices  
  - `available_product.csv`: broader market/supplier universe  
  - `orders.csv`: historical and recent orders  
  - Transcript JSON files for example agent calls (in `data/transcripts/` and `transcripts/`)

---

## How to Test It

### Prerequisites

Before getting started, you'll need:
- Python 3.10 or higher
- Node.js and npm
- A Mistral AI API key (get one at [console.mistral.ai](https://console.mistral.ai/))

### Step 1: Configure Your API Keys

Create a `.env` file in the **backend** directory with your Mistral API key:

```bash
cd backend
cat > .env << EOF
MISTRAL_API_KEY=your_mistral_api_key_here
EOF
```

This key is essential for the AI-powered conversation parsing feature.

### Step 2: Install Dependencies

From the project root, install all dependencies using make:

```bash
make install
```

This will install both backend (Python) and frontend (Node.js) dependencies.

### Step 3: Launch the Application

Start both the backend API and the frontend UI:

```bash
make dev
```

The application will be available at:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

You can now explore the Control Tower dashboard, view supplier analytics, and see AI-powered insights!

### Step 4: Test the Mistral AI Parser (Recommended)

To see Mistral AI in action, test the conversation parser that analyzes supplier call transcripts:

```bash
make test-parser
```

This will:
- Parse a sample phone conversation with a supplier
- Extract structured information (product names, prices, delivery times)
- Demonstrate how Mistral AI understands and structures unstructured conversations

This is the **core feature** that showcases the power of Mistral AI in automating procurement workflows.

### Optional: Test AI Phone Calls with ElevenLabs (Advanced)

If you want to test the complete AI phone agent that can actually call suppliers:

#### Prerequisites
- An ElevenLabs API key (get one at [elevenlabs.io](https://elevenlabs.io/))
- A Twilio phone number configured for voice calls
- ElevenLabs Conversational AI agent configured in your [ElevenLabs Studio](https://elevenlabs.io/app/conversational-ai)

#### Configuration

Add your ElevenLabs API key to the `.env` file in the **backend** directory:

```bash
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

#### Create an AI Agent

Run the agent creation script to set up an AI phone agent:

```bash
cd elevenlabsdemo
python create_agent.py
```

This will create a conversational AI agent configured to:
- Answer incoming calls from suppliers
- Ask about product updates, pricing changes, and delivery times
- Record and transcribe the entire conversation

#### Connect to Twilio

1. In your [Twilio Console](https://console.twilio.com/), configure your phone number's webhook
2. Point the voice webhook to your ElevenLabs agent endpoint
3. Set up the ElevenLabs agent in your [ElevenLabs Studio](https://elevenlabs.io/app/conversational-ai) with the Twilio integration

#### Make a Test Call

Once configured, you can:
- Call your Twilio number to simulate a supplier call
- The AI agent will answer and conduct a conversation
- The transcript is automatically parsed by Mistral AI
- Product updates are extracted and saved to the database

This demonstrates the complete end-to-end workflow: AI phone agent → conversation transcript → Mistral AI parsing → structured data extraction.

---

## Next Steps

Natural next steps:
- Persist agent decisions back into a real ERP/inventory system.
- Extend the parsing pipeline to handle email threads and PDFs, not just call transcripts.
- Add role-based dashboards for finance, operations, and category managers.