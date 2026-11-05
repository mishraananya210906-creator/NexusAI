
import { useState } from "react";
import "./App.css";

const API_BASE_URL = "https://nexusai-8rmm.onrender.com";

function App() {
  const [activeTab, setActiveTab] = useState("Dashboard");

  // AI Assistant states
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Support Ticket states
  const [ticket, setTicket] = useState("");
  const [ticketLoading, setTicketLoading] = useState(false);
  const [ticketResult, setTicketResult] = useState(null);
  const [ticketError, setTicketError] = useState("");

  const menuItems = [
    { name: "Dashboard", icon: "▦" },
    { name: "AI Assistant", icon: "✧" },
    { name: "Support Tickets", icon: "▤" },
    { name: "Analytics", icon: "◫" },
  ];

  // ==========================================
  // AI ASSISTANT
  // ==========================================

  async function sendMessage(e) {
    e.preventDefault();

    const userQuestion = question.trim();

    if (!userQuestion || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", text: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data)
        );
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.answer,
          citations: data.citations || [],
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: `Sorry, something went wrong: ${error.message}`,
          citations: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // ==========================================
  // SUPPORT TICKET CLASSIFICATION
  // ==========================================

  async function classifyTicket(e) {
    e.preventDefault();

    const ticketText = ticket.trim();

    if (!ticketText || ticketLoading) return;

    setTicketLoading(true);
    setTicketResult(null);
    setTicketError("");

    try {
      const response = await fetch(`${API_BASE_URL}/triage`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ticket: ticketText,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || data)
        );
      }

      setTicketResult(data);
    } catch (error) {
      setTicketError(error.message);
    } finally {
      setTicketLoading(false);
    }
  }

  function clearTicket() {
    setTicket("");
    setTicketResult(null);
    setTicketError("");
  }

  // ==========================================
  // ANALYTICS DATA
  // ==========================================

  const categoryData = [
    { name: "Account", count: 20 },
    { name: "Billing", count: 20 },
    { name: "Bug", count: 20 },
    { name: "Subscription", count: 20 },
    { name: "API", count: 20 },
  ];

  const priorityData = [
    { name: "High", count: 28 },
    { name: "Medium", count: 39 },
    { name: "Low", count: 33 },
  ];

  // ==========================================
  // MAIN APPLICATION
  // ==========================================

  return (
    <div className="app-container">

      {/* SIDEBAR */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">N</div>
          <div>
            <h2>NexusAI</h2>
            <span>INTELLIGENT SUPPORT</span>
          </div>
        </div>

        <p className="menu-heading">WORKSPACE</p>

        <nav>
          {menuItems.map((item) => (
            <button
              key={item.name}
              className={`menu-item ${
                activeTab === item.name ? "active" : ""
              }`}
              onClick={() => setActiveTab(item.name)}
            >
              <span>{item.icon}</span>
              {item.name}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="user-avatar">A</div>
          <div>
            <strong>Admin User</strong>
            <span>Administrator</span>
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT */}

      <main className="main-content">

        <header className="topbar">
          <div>
            <p className="breadcrumb">
              Workspace / {activeTab}
            </p>
            <h1>{activeTab}</h1>
          </div>

          <div className="topbar-right">
            <span className="status-dot"></span>
            System Online
            <div className="profile-avatar">A</div>
          </div>
        </header>

        {/* DASHBOARD */}

        {activeTab === "Dashboard" && (
          <>
            <section className="welcome-section">
              <div>
                <p className="eyebrow">
                  YOUR AI SUPPORT WORKSPACE
                </p>

                <h2>Welcome to NexusAI 👋</h2>

                <p>
                  Intelligent customer support, powered by machine
                  learning and retrieval-augmented generation.
                </p>
              </div>

              <div className="welcome-icon">✧</div>
            </section>

            <section className="stats-grid">

              <div className="stat-card">
                <span>Total Tickets</span>
                <h2>100</h2>
                <p>Dataset records</p>
              </div>

              <div className="stat-card">
                <span>Ticket Categories</span>
                <h2>05</h2>
                <p>Classification groups</p>
              </div>

              <div className="stat-card">
                <span>Category Accuracy</span>
                <h2>84%</h2>
                <p>Evaluation result</p>
              </div>

            </section>

            <section className="content-grid">

              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">AI POWERED</p>
                    <h3>AI Support Assistant</h3>
                  </div>

                  <span className="ai-symbol">✧</span>
                </div>

                <div className="assistant-placeholder">
                  <div className="bot-icon">✧</div>

                  <h3>How can I help you today?</h3>

                  <p>
                    Ask questions about accounts, billing,
                    payments and subscriptions.
                  </p>

                  <button
                    className="primary-button"
                    onClick={() => setActiveTab("AI Assistant")}
                  >
                    Open AI Assistant →
                  </button>
                </div>
              </div>

              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">
                      SMART CLASSIFICATION
                    </p>
                    <h3>Support Ticket Triage</h3>
                  </div>

                  <span className="ticket-symbol">▤</span>
                </div>

                <p className="panel-description">
                  Automatically identify ticket categories,
                  priorities and support departments.
                </p>

                <div className="ticket-types">
                  <span>Account</span>
                  <span>Billing</span>
                  <span>Bug</span>
                  <span>API</span>
                  <span>Subscription</span>
                </div>

                <button
                  className="secondary-button"
                  onClick={() => setActiveTab("Support Tickets")}
                >
                  Classify a Ticket →
                </button>
              </div>

            </section>
          </>
        )}

        {/* AI ASSISTANT */}

        {activeTab === "AI Assistant" && (
          <section className="panel chat-panel">

            <div className="panel-heading">
              <div>
                <p className="eyebrow">RAG POWERED SUPPORT</p>
                <h3>NexusAI Assistant</h3>
              </div>

              <span className="ai-symbol">✧</span>
            </div>

            <div className="chat-messages">

              {messages.length === 0 && (
                <div className="chat-welcome">
                  <div className="bot-icon">✧</div>

                  <h3>How can I help you today?</h3>

                  <p>
                    Ask me about account access, billing,
                    payments or subscriptions.
                  </p>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  className={`chat-message ${message.role}`}
                  key={index}
                >
                  <strong>
                    {message.role === "user" ? "You" : "NexusAI"}
                  </strong>

                  <p>{message.text}</p>

                  {message.citations?.length > 0 && (
                    <div className="citations">
                      <strong>Sources</strong>

                      {message.citations.map((citation, i) => (
                        <p key={i}>
                          {citation.filename}
                          {citation.page
                            ? ` — Page ${citation.page}`
                            : ""}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="chat-message assistant">
                  <strong>NexusAI</strong>
                  <p>Searching support documents...</p>
                </div>
              )}

            </div>

            <form
              className="chat-form"
              onSubmit={sendMessage}
            >
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Type your support question..."
                maxLength={1000}
                disabled={loading}
              />

              <button
                type="submit"
                className="primary-button"
                disabled={loading || !question.trim()}
              >
                {loading ? "Sending..." : "Send →"}
              </button>
            </form>

            <p className="chat-note">
              Answers are retrieved from the available support documents.
            </p>

          </section>
        )}

        {/* SUPPORT TICKETS */}

        {activeTab === "Support Tickets" && (
          <>

            <section className="ticket-intro">
              <p className="eyebrow">MACHINE LEARNING POWERED</p>

              <h2>Intelligent Ticket Classification</h2>

              <p>
                Enter a customer support issue and let NexusAI
                automatically identify its category, priority
                and responsible department.
              </p>
            </section>

            <section className="panel ticket-classifier">

              <div className="panel-heading">
                <div>
                  <p className="eyebrow">TICKET ANALYSIS</p>
                  <h3>Classify a Support Ticket</h3>
                </div>

                <span className="ticket-symbol">▤</span>
              </div>

              <form onSubmit={classifyTicket}>

                <label className="ticket-label">
                  Customer Issue
                </label>

                <textarea
                  className="ticket-textarea"
                  value={ticket}
                  onChange={(e) => setTicket(e.target.value)}
                  placeholder="Example: I cannot log into my account. The application says my password is incorrect."
                  minLength={5}
                  maxLength={2000}
                  rows={6}
                  disabled={ticketLoading}
                  required
                />

                <div className="ticket-form-footer">
                  <span>
                    {ticket.length}/2000 characters
                  </span>

                  <div className="ticket-actions">

                    <button
                      type="button"
                      className="secondary-button"
                      onClick={clearTicket}
                      disabled={ticketLoading}
                    >
                      Clear
                    </button>

                    <button
                      type="submit"
                      className="primary-button"
                      disabled={
                        ticketLoading || ticket.trim().length < 5
                      }
                    >
                      {ticketLoading
                        ? "Analyzing..."
                        : "Analyze Ticket →"}
                    </button>

                  </div>
                </div>

              </form>

              {ticketError && (
                <div className="ticket-error">
                  <strong>Classification failed</strong>
                  <p>{ticketError}</p>
                </div>
              )}

            </section>

            {ticketResult && (
              <section className="panel ticket-results">

                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">ANALYSIS COMPLETE</p>
                    <h3>Classification Results</h3>
                  </div>

                  <span className="result-success">✓ Complete</span>
                </div>

                <div className="ticket-result-grid">

                  <div className="result-card">
                    <span>Predicted Category</span>
                    <h2>
                      {ticketResult.category || "Not available"}
                    </h2>
                  </div>

                  <div className="result-card">
                    <span>Predicted Priority</span>
                    <h2>
                      {ticketResult.priority || "Not available"}
                    </h2>
                  </div>

                  <div className="result-card">
                    <span>Assigned Department</span>
                    <h2>
                      {ticketResult.department || "Not available"}
                    </h2>
                  </div>

                </div>

                <div className="result-ticket-text">
                  <strong>Analyzed Ticket</strong>
                  <p>
                    {ticketResult.ticket || ticket}
                  </p>
                </div>

                <button
                  className="secondary-button"
                  onClick={clearTicket}
                >
                  Classify Another Ticket →
                </button>

              </section>
            )}

            {!ticketResult && !ticketError && (
              <section className="ticket-info">
                <p className="eyebrow">SUPPORTED CATEGORIES</p>

                <div className="ticket-types">
                  <span>Account</span>
                  <span>Billing</span>
                  <span>Bug</span>
                  <span>Subscription</span>
                  <span>API</span>
                </div>

                <p>
                  NexusAI uses its trained machine learning
                  classification models to analyze support tickets.
                </p>
              </section>
            )}

          </>
        )}

        {/* ANALYTICS DASHBOARD */}

        {activeTab === "Analytics" && (
          <section className="panel analytics-page">

            <div className="analytics-header">
              <div>
                <p className="eyebrow">PERFORMANCE INSIGHTS</p>
                <h3>Analytics Overview</h3>
                <p className="panel-description">
                  Insights into ticket distribution and ML model performance.
                </p>
              </div>

              <span className="analytics-tag">
                Dataset: 100 Tickets
              </span>
            </div>

            <div className="analytics-summary-grid">

              <div className="analytics-card">
                <span>Category Classifier Accuracy</span>
                <h2>84%</h2>
                <p>TF-IDF + Logistic Regression</p>
              </div>

              <div className="analytics-card">
                <span>Priority Classifier Accuracy</span>
                <h2>60%</h2>
                <p>TF-IDF + Logistic Regression</p>
              </div>

              <div className="analytics-card">
                <span>Total Dataset Tickets</span>
                <h2>100</h2>
                <p>Five support categories</p>
              </div>

            </div>

            <div className="analytics-section">
              <h3>Ticket Category Distribution</h3>

              <p className="panel-description">
                Distribution across the five ticket categories.
              </p>

              {categoryData.map((item) => (
                <div
                  className="analytics-bar-row"
                  key={item.name}
                >
                  <div className="analytics-bar-label">
                    <span>{item.name}</span>
                    <span>{item.count}%</span>
                  </div>

                  <div className="analytics-bar-track">
                    <div
                      className="analytics-bar-fill"
                      style={{ width: `${item.count}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="analytics-section">
              <h3>Ticket Priority Distribution</h3>

              <p className="panel-description">
                Breakdown of ticket priorities in the dataset.
              </p>

              {priorityData.map((item) => (
                <div
                  className="analytics-bar-row"
                  key={item.name}
                >
                  <div className="analytics-bar-label">
                    <span>{item.name}</span>
                    <span>{item.count}%</span>
                  </div>

                  <div className="analytics-bar-track">
                    <div
                      className="analytics-bar-fill"
                      style={{ width: `${item.count}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            <div className="analytics-section">
              <h3>Model Evaluation</h3>

              <div className="analytics-metrics-grid">

                <div className="analytics-metric">
                  <span>Category Macro F1-Score</span>
                  <h2>0.8367</h2>
                </div>

                <div className="analytics-metric">
                  <span>Priority Macro F1-Score</span>
                  <h2>0.5931</h2>
                </div>

              </div>
            </div>

            <p className="analytics-disclaimer">
              Note: These are preliminary evaluation results from a
              small synthetic 100-ticket dataset. Performance may
              vary on real-world support tickets.
            </p>

          </section>
        )}

        {/* FOOTER */}

        <footer>
          <span>NexusAI © 2026</span>
          <span>Intelligent Support Assistant</span>
        </footer>

      </main>
    </div>
  );
}

export default App;
