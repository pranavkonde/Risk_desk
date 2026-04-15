const TESTNET = "https://test-api.pacifica.fi/api/v1";
const MAINNET = "https://api.pacifica.fi/api/v1";

export function baseUrl(network: string): string {
  return network === "mainnet" ? MAINNET : TESTNET;
}

export async function getJson(path: string, network: string): Promise<any> {
  const url = `${baseUrl(network).replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
  const res = await fetch(url, { cache: "no-store" });
  const text = await res.text();
  let body: any = text;
  try {
    body = JSON.parse(text);
  } catch {
    // Keep text for clearer upstream errors.
  }
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${typeof body === "string" ? body : JSON.stringify(body)}`);
  }
  if (typeof body === "object" && body && body.success === false) {
    throw new Error(`Pacifica error: ${body.error ?? "Unknown error"}`);
  }
  return body;
}
