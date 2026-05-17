"""Async job client for large-document extraction via Mawlaia DocParse API."""
from __future__ import annotations
import time
from typing import Optional
import httpx

_DEFAULT_BASE = "https://api.mawlaia.com"


class AsyncJobClient:
    """
    Submit DocParse extraction jobs and poll for results.
    Use this for large PDFs (>1000 words) where the sync /extract endpoint may time out.

    Example::

        from docparse import AsyncJobClient

        client = AsyncJobClient(api_key="mwl_live_...")

        job = client.submit(text=pdf_text, schema_name="contract",
                            webhook_url="https://yourapp.com/hooks/docparse")
        print(job["job_id"], job["status"])  # pending

        # Poll until done (or use webhook)
        result = client.wait(job["job_id"], timeout=120)
        print(result["result"])  # {"parties": {"value": [...], "confidence": 0.97}, ...}
    """

    def __init__(self, api_key: str, base_url: str = _DEFAULT_BASE, timeout: float = 15.0):
        self._base    = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        self._timeout = timeout

    def submit(
        self,
        text:        str,
        schema_name: Optional[str] = None,
        fields:      Optional[list[dict]] = None,
        webhook_url: Optional[str] = None,
    ) -> dict:
        """Submit a job. Returns immediately with ``{"job_id": ..., "status": "pending"}``."""
        payload: dict = {"text": text}
        if schema_name:
            payload["schema_name"] = schema_name
        if fields:
            payload["fields"] = fields
        if webhook_url:
            payload["webhook_url"] = webhook_url

        with httpx.Client(base_url=self._base, headers=self._headers, timeout=self._timeout) as c:
            r = c.post("/v1/doc/jobs", json=payload)
            r.raise_for_status()
            return r.json()

    def poll(self, job_id: str) -> dict:
        """Fetch current status of a job."""
        with httpx.Client(base_url=self._base, headers=self._headers, timeout=self._timeout) as c:
            r = c.get(f"/v1/doc/jobs/{job_id}")
            r.raise_for_status()
            return r.json()

    def list_jobs(self) -> list[dict]:
        """Return the 20 most recent jobs for this API key."""
        with httpx.Client(base_url=self._base, headers=self._headers, timeout=self._timeout) as c:
            r = c.get("/v1/doc/jobs")
            r.raise_for_status()
            return r.json()

    def wait(self, job_id: str, timeout: float = 120.0, poll_interval: float = 2.0) -> dict:
        """
        Block until the job is ``completed`` or ``failed``, then return the job dict.
        Raises ``TimeoutError`` if *timeout* seconds elapse first.
        """
        deadline = time.monotonic() + timeout
        while True:
            job = self.poll(job_id)
            if job["status"] in ("completed", "failed"):
                return job
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Job {job_id} not finished within {timeout}s")
            time.sleep(poll_interval)
