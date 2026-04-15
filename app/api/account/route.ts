import { NextRequest, NextResponse } from "next/server";
import { getJson } from "@/lib/pacifica";

export async function GET(req: NextRequest) {
  const network = req.nextUrl.searchParams.get("network") ?? "testnet";
  const account = req.nextUrl.searchParams.get("account");
  if (!account) {
    return NextResponse.json({ error: "account is required" }, { status: 400 });
  }
  try {
    const data = await getJson(`/account?account=${encodeURIComponent(account)}`, network);
    return NextResponse.json(data.data ?? {});
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 },
    );
  }
}
