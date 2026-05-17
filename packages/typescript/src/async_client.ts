export interface AsyncJobClientOptions {
  apiKey: string;
  baseUrl?: string;
  timeout?: number;
}

export interface DocparseJob {
  job_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  schema_name?: string;
  result?: Record<string, unknown>;
  error?: string;
  created_at: string;
  completed_at?: string;
}

export class AsyncJobClient {
  private readonly base: string;
  private readonly headers: Record<string, string>;
  private readonly timeout: number;

  constructor({ apiKey, baseUrl = "https://api.mawlaia.com", timeout = 15_000 }: AsyncJobClientOptions) {
    this.base = baseUrl.replace(/\/$/, "");
    this.headers = {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    };
    this.timeout = timeout;
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), this.timeout);
    try {
      const res = await fetch(`${this.base}${path}`, {
        method,
        headers: this.headers,
        body: body !== undefined ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });
      if (!res.ok) throw new Error(`Mawlaia API error: ${res.status} ${await res.text()}`);
      return res.json() as Promise<T>;
    } finally {
      clearTimeout(id);
    }
  }

  async submit(
    text: string,
    options: { schemaName?: string; fields?: Record<string, unknown>[]; webhookUrl?: string } = {},
  ): Promise<{ job_id: string; status: "pending" }> {
    const body: Record<string, unknown> = { text };
    if (options.schemaName) body.schema_name = options.schemaName;
    if (options.fields)     body.fields      = options.fields;
    if (options.webhookUrl) body.webhook_url  = options.webhookUrl;
    return this.request("POST", "/v1/doc/jobs", body);
  }

  async poll(jobId: string): Promise<DocparseJob> {
    return this.request("GET", `/v1/doc/jobs/${jobId}`);
  }

  async listJobs(): Promise<DocparseJob[]> {
    return this.request("GET", "/v1/doc/jobs");
  }

  async wait(jobId: string, timeoutMs = 120_000, pollIntervalMs = 2_000): Promise<DocparseJob> {
    const deadline = Date.now() + timeoutMs;
    while (true) {
      const job = await this.poll(jobId);
      if (job.status === "completed" || job.status === "failed") return job;
      if (Date.now() >= deadline) throw new Error(`Job ${jobId} not finished within ${timeoutMs}ms`);
      await new Promise((r) => setTimeout(r, pollIntervalMs));
    }
  }
}
