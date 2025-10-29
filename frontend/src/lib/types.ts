export type Article = {
  id: string;
  title: string;
  url: string;
  source: {
    name: string;
    url: string;
    favicon?: string;
  };
  summary: string;
  tags: string[];
  categories: string[];
  vendors: string[];
  publishedAt: string;
};

export type FilterParams = {
  search?: string;
  categories?: string[];
  vendors?: string[];
  dateRange?: "24h" | "7d" | "30d";
  page?: number;
};

export const CATEGORIES = [
  "Research",
  "Product",
  "Safety",
  "Policy",
  "Open Source",
  "Startups",
  "Ecosystem",
];

export const VENDORS = [
  "OpenAI",
  "Google",
  "Meta",
  "Anthropic",
  "Mistral",
  "xAI",
  "Cohere",
  "Stability",
];
