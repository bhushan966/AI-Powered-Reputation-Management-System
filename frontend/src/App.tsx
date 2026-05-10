import { useState } from 'react';
import type { AggregatedResult, SearchPayload } from './types';
import './index.css';

const defaultPrompt = 'Enter a restaurant or hotel name to see reputation insights.';

export default function App() {
  const [business, setBusiness] = useState('');
  const [location, setLocation] = useState('');
  const [website, setWebsite] = useState('');
  const [result, setResult] = useState<AggregatedResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setIsLoading(true);

    const payload: SearchPayload = {
      businessName: business,
      location,
      website,
    };

    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error('Failed to fetch reputation data');
      }
      const body = await response.json();
      setResult(body as AggregatedResult);
    } catch (err) {
      setError((err as Error).message);
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <h1>Reputation Pulse</h1>
          <p>AI-powered reputation dashboard for restaurants and hotels. Aggregate customer reviews, sentiment, summaries, and response suggestions.</p>
        </div>
      </section>

      <section className="search-panel">
        <form onSubmit={handleSubmit} className="search-form">
          <div className="field-row">
            <label>Business name</label>
            <input value={business} onChange={(e) => setBusiness(e.target.value)} placeholder="e.g. Olive Garden" required />
          </div>
          <div className="field-row">
            <label>City / location</label>
            <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="e.g. Mumbai" required />
          </div>
          <div className="field-row">
            <label>Website / URL (optional)</label>
            <input value={website} onChange={(e) => setWebsite(e.target.value)} placeholder="https://" />
          </div>
          <button type="submit" disabled={isLoading}>Search reputation</button>
        </form>
        {error ? <div className="error-box">{error}</div> : null}
      </section>

      {isLoading && <section className="status-card">Loading reputation data...</section>}

      {!result && !isLoading ? (
        <section className="status-card">{defaultPrompt}</section>
      ) : null}

      {result ? (
        <section className="dashboard-grid">
          <div className="stat-card">
            <h2>Total reviews</h2>
            <p>{result.summary.totalReviews}</p>
          </div>
          <div className="stat-card">
            <h2>Average rating</h2>
            <p>{result.summary.averageRating.toFixed(1)}</p>
          </div>
          <div className="stat-card">
            <h2>Sentiment split</h2>
            <p>Positive: {result.summary.sentimentSplit.positive}</p>
            <p>Neutral: {result.summary.sentimentSplit.neutral}</p>
            <p>Negative: {result.summary.sentimentSplit.negative}</p>
          </div>
          <div className="stat-card">
            <h2>Top complaints</h2>
            <ol>
              {result.summary.topComplaints.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ol>
          </div>
          <div className="stat-card">
            <h2>Top compliments</h2>
            <ol>
              {result.summary.topCompliments.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ol>
          </div>
          <div className="stat-card">
            <h2>Recommendations</h2>
            <ul>
              {result.recommendations.map((item, index) => {
                const text = typeof item === 'object' ? Object.values(item).join(' - ') : String(item);
                return <li key={index}>{text}</li>;
              })}
            </ul>
          </div>
        </section>
      ) : null}

      {result ? (
        <section className="reviews-panel">
          <div className="section-header">
            <h2>Recent reviews & mentions</h2>
          </div>
          {result.reviews.map((review) => (
            <article className="review-card" key={review.id}>
              <header>
                <strong>{review.source}</strong>
                <span className={`pill ${review.sentiment.toLowerCase()}`}>{review.sentiment}</span>
              </header>
              <p>{review.message}</p>
              <div className="review-meta">
                <span>Rating: {review.rating ?? 'N/A'}</span>
                <span>Topic: {review.topic}</span>
                <span>Emotion: {review.emotion}</span>
                <span>Priority: {review.priority}</span>
              </div>
              <button
                className="response-button"
                onClick={async () => {
                  const res = await fetch('http://localhost:8000/api/respond', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ reviewText: review.message, sentiment: review.sentiment }),
                  });
                  const data = await res.json();
                  alert(`Suggested response:\n\n${data.response}`);
                }}
              >
                Generate response
              </button>
            </article>
          ))}
        </section>
      ) : null}
    </main>
  );
}
