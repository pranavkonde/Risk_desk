import { NextRequest, NextResponse } from "next/server";
import { getJson } from "@/lib/pacifica";

export async function GET(req: NextRequest) {
  const network = req.nextUrl.searchParams.get("network") ?? "testnet";
  const account = req.nextUrl.searchParams.get("account");
  const limit = req.nextUrl.searchParams.get("limit") ?? "120";
  if (!account) {
    return NextResponse.json({ error: "account is required" }, { status: 400 });
  }
  try {
    const data = await getJson(
      `/trades/history?account=${encodeURIComponent(account)}&limit=${encodeURIComponent(limit)}`,
      network,
    );
    return NextResponse.json({
      data: data.data ?? [],
      has_more: Boolean(data.has_more),
      next_cursor: data.next_cursor ?? null,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 },
    );
  }
}
