import { NextRequest, NextResponse } from "next/server";
import { getJson } from "@/lib/pacifica";

export async function GET(req: NextRequest) {
  const network = req.nextUrl.searchParams.get("network") ?? "testnet";
  const symbol = req.nextUrl.searchParams.get("symbol") ?? "BTC";
  try {
    const data = await getJson(`/book?symbol=${encodeURIComponent(symbol)}`, network);
    return NextResponse.json(data.data ?? {});
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 },
    );
  }
}
