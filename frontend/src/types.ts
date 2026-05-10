export type SentimentValue = 'Positive' | 'Neutral' | 'Negative';

export type PriorityValue = 'High' | 'Medium' | 'Low';

export type EmotionValue = 'Happy' | 'Impressed' | 'Frustrated' | 'Disappointed' | 'Neutral';

export interface ReviewRecord {
  id: string;
  source: string;
  author: string;
  rating: number | null;
  message: string;
  publishedAt: string;
  sentiment: SentimentValue;
  topic: string;
  emotion: EmotionValue;
  priority: PriorityValue;
}

export interface AggregatedSummary {
  totalReviews: number;
  averageRating: number;
  sentimentSplit: {
    positive: number;
    neutral: number;
    negative: number;
  };
  topComplaints: string[];
  topCompliments: string[];
}

export interface AggregatedResult {
  businessName: string;
  location: string;
  reviews: ReviewRecord[];
  summary: AggregatedSummary;
  recommendations: string[];
}

export interface SearchPayload {
  businessName: string;
  location: string;
  website?: string;
}

export interface ResponsePayload {
  reviewText: string;
  sentiment: SentimentValue;
}
