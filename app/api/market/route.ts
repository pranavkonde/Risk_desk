import { NextRequest, NextResponse } from "next/server";
import { getJson } from "@/lib/pacifica";

export async function GET(req: NextRequest) {
  const network = req.nextUrl.searchParams.get("network") ?? "testnet";
  try {
    const [info, prices] = await Promise.all([
      getJson("/info", network),
      getJson("/info/prices", network),
    ]);
    return NextResponse.json({
      info: info.data ?? [],
      prices: prices.data ?? [],
    });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 },
    );
  }
}
